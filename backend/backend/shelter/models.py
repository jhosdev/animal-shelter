from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Administrator'),
        ('VOLUNTEER', 'Volunteer'),
        ('ADOPTER', 'Adopter'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, default='ACTIVE')
    REQUIRED_FIELDS = ['role', 'email']


class Animal(models.Model):
    ANIMAL_TYPES = (
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
    )
    ANIMAL_STATUS = (
        ('AVAILABLE', 'Available for adoption'),
        ('ADOPTED', 'Adopted'),
        ('PENDING', 'Pending adoption'),
    )
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    breed = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=3, choices=ANIMAL_TYPES)
    status = models.CharField(max_length=10, choices=ANIMAL_STATUS, default='AVAILABLE')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='animals_created')


class Adoption(models.Model):
    ADOPTION_STATUS = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    adopter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoptions')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='processed_adoptions')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=ADOPTION_STATUS, default='PENDING')
