from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Animal, Adoption
from .serializers import UserSerializer, AnimalSerializer, AdoptionSerializer
from .permissions import IsAdminUser, IsVolunteerUser, IsAdopterUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAdminUser | IsVolunteerUser]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'VOLUNTEER':
            return User.objects.filter(role='ADOPTER')
        return User.objects.all()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by('id')
    serializer_class = AnimalSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsAdminUser | IsVolunteerUser]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        user = self.request.user
        #if user.role != 'VOLUNTEER':
        #    raise serializers.ValidationError("Only volunteers can create animals.")
        serializer.save(volunteer=user)

    @action(detail=True, methods=['post'], permission_classes=[IsVolunteerUser])
    def change_status(self, request, pk=None):
        animal = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Animal.ANIMAL_STATUS).keys():
            animal.status = new_status
            animal.save()
            return Response({'status': 'animal status updated'})
        return Response({'status': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)


class AdoptionViewSet(viewsets.ModelViewSet):
    queryset = Adoption.objects.all().order_by('id')
    serializer_class = AdoptionSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdopterUser]
        elif self.action in ['list', 'retrieve', 'partial_update']:
            permission_classes = [IsAdminUser | IsVolunteerUser]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(adopter=self.request.user)
