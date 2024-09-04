from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User, Animal, Adoption
from .serializers import UserSerializer, AnimalSerializer, AdoptionSerializer

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'ADOPTER'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        url = reverse('user-list')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'role': 'ADOPTER'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertEqual(serializer.data['email'], 'test@example.com')
        self.assertNotIn('password', serializer.data)

class AnimalTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='volunteer', email='volunteer@example.com', password='pass123', role='VOLUNTEER')
        self.client.force_authenticate(user=self.user)
        self.animal_data = {
            'name': 'Buddy',
            'age': 3,
            'breed': 'Labrador',
            'animal_type': 'DOG',
            'status': 'AVAILABLE',
            'volunteer': self.user
        }
        self.animal = Animal.objects.create(**self.animal_data)

    def test_create_animal(self):
        url = reverse('animal-list')
        data = self.animal_data.copy()
        data['volunteer'] = self.user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Animal.objects.count(), 2)

    def test_update_animal_status(self):
        url = reverse('animal-detail', kwargs={'pk': self.animal.id})
        data = {'status': 'PENDING'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, 'PENDING')
        self.assertEqual(Adoption.objects.count(), 1)

class AdoptionTests(APITestCase):
    def setUp(self):
        self.volunteer = User.objects.create_user(username='volunteer', email='volunteer@example.com', password='pass123', role='VOLUNTEER')
        self.adopter = User.objects.create_user(username='adopter', email='adopter@example.com', password='pass123', role='ADOPTER')
        self.animal = Animal.objects.create(name='Fluffy', age=2, breed='Persian', animal_type='CAT', status='AVAILABLE', volunteer=self.volunteer)

    def test_create_adoption(self):
        self.client.force_authenticate(user=self.adopter)
        url = reverse('adoption-list')
        data = {'animal': self.animal.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Adoption.objects.count(), 1)
        self.animal.refresh_from_db()
        self.assertEqual(self.animal.status, 'PENDING')

    def test_update_adoption_status_as_adopter(self):
        self.client.force_authenticate(user=self.adopter)
        adoption = Adoption.objects.create(animal=self.animal, adopter=self.adopter, volunteer=self.volunteer, status='PENDING')
        url = reverse('adoption-detail', kwargs={'pk': adoption.id})
        data = {'status': 'COMPLETED'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ModelTests(TestCase):
    def test_user_model(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123', role='ADOPTER')
        self.assertEqual(str(user), 'testuser')
        self.assertEqual(user.role, 'ADOPTER')

    def test_animal_model(self):
        volunteer = User.objects.create_user(username='volunteer', email='volunteer@example.com', password='pass123', role='VOLUNTEER')
        animal = Animal.objects.create(name='Rex', age=4, breed='German Shepherd', animal_type='DOG', status='AVAILABLE', volunteer=volunteer)
        self.assertEqual(str(animal.name), 'Rex')
        self.assertEqual(animal.status, 'AVAILABLE')

    def test_adoption_model(self):
        volunteer = User.objects.create_user(username='volunteer', email='volunteer@example.com', password='pass123', role='VOLUNTEER')
        adopter = User.objects.create_user(username='adopter', email='adopter@example.com', password='pass123', role='ADOPTER')
        animal = Animal.objects.create(name='Whiskers', age=1, breed='Siamese', animal_type='CAT', status='AVAILABLE', volunteer=volunteer)
        adoption = Adoption.objects.create(animal=animal, adopter=adopter, volunteer=volunteer, status='PENDING')
        self.assertEqual(adoption.status, 'PENDING')
        self.assertEqual(adoption.animal, animal)
        self.assertEqual(adoption.adopter, adopter)