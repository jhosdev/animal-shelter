import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    User, Role, UserDetails, Pet, Notification,
    Subscription, Payment, Device, UsageLog, Habit
)
from .serializers import (
    SignUpSerializer, UserSerializer, RoleSerializer, UserDetailsSerializer, PetSerializer, NotificationSerializer,
    SubscriptionSerializer, PaymentSerializer, DeviceSerializer, UsageLogSerializer, HabitSerializer
)

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

# IAM
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Profiles
class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all()
    serializer_class = UserDetailsSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset


# Pets
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer


# Communications
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset


# Subscriptions & Billing
class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(user__id=user_id)
        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


# Tracking
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_authenticators(self):
        """
        Skip JWT authentication for public endpoints.
        """
        iot_device_api_key = self.request.headers.get('iot-device-api-key')
        if self.request.method == 'GET' and (
            'serial_number' in self.request.GET or
            self.kwargs.get('pk')  # For /device/{id} endpoint
        ) and iot_device_api_key == os.getenv('IOT_DEVICE_API_KEY'):
            return []
        if self.request.method == 'PATCH' and iot_device_api_key == os.getenv('IOT_DEVICE_API_KEY'):
            return []
        return super().get_authenticators()

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(pet__user__id=user_id)
        serial_number = self.request.query_params.get('serial_number', None)
        if serial_number:
            queryset = queryset.filter(serial_number=serial_number)
        return queryset


class UsageLogViewSet(viewsets.ModelViewSet):
    queryset = UsageLog.objects.all()
    serializer_class = UsageLogSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(device__pet__user__id=user_id)
        return queryset

class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class SignUpViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Allow any user to sign up

    def create(self, request):
        """
        Handle user sign up. Create a new user and user details.
        """
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User created successfully',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'role': user.role.id,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)