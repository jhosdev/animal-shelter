import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    User, Role, UserDetails, Pet, Notification,
    Subscription, Payment, Device, UsageLog, Habit
)
from .serializers import (
    ModifyQuantitySerializer, SignUpSerializer, UserSerializer, RoleSerializer, UserDetailsSerializer, PetSerializer, NotificationSerializer,
    SubscriptionSerializer, PaymentSerializer, DeviceSerializer, UsageLogSerializer, HabitSerializer
)

from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from django.utils import timezone

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
        if self.request is  None:
            return []
        iot_device_api_key = self.request.headers.get('iot-device-api-key')
        if self.request.method == 'GET' and (
            'serial_number' in self.request.GET or
            self.kwargs.get('pk')  # For /device/{id} endpoint
        ) and iot_device_api_key == os.getenv('IOT_DEVICE_API_KEY'):
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
        device_id = self.request.query_params.get('device_id')
        if device_id:
            queryset = queryset.filter(device__id=device_id)
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
    

class UpdateDeviceQuantityViewSet(viewsets.ViewSet):

    def get_authenticators(self):
        """
        Skip JWT authentication for public endpoints.
        """
        if self.request is  None:
            return []
        iot_device_api_key = self.request.headers.get('iot-device-api-key')
        if iot_device_api_key == os.getenv('IOT_DEVICE_API_KEY'):
            return []
        return super().get_authenticators()
    
    def create(self, request):
        # Deserialize the request data
        serializer = ModifyQuantitySerializer(data=request.data)
        if serializer.is_valid():
            device_id = serializer.validated_data['device_id']
            type = serializer.validated_data['type']
            quantity = serializer.validated_data['quantity']
            action = serializer.validated_data['action']

            # Check if the device exists
            try:
                device = Device.objects.get(id=device_id)
            except Device.DoesNotExist:
                raise NotFound(detail="Device not found")

            # Adjust the quantity based on action
            if action == 'add':
                if type == 'food':
                    new_food_quantity = device.food_quantity + quantity
                    if new_food_quantity > device.food_limit:
                        raise ValidationError("Food quantity cannot exceed the food limit.")
                    device.food_quantity = new_food_quantity

                elif type == 'water':
                    new_water_quantity = device.water_quantity + quantity
                    if new_water_quantity > device.water_limit:
                        raise ValidationError("Water quantity cannot exceed the water limit.")
                    device.water_quantity = new_water_quantity

            elif action == 'subtract':
                if type == 'food':
                    new_food_quantity = device.food_quantity - quantity
                    if new_food_quantity < 0:
                        raise ValidationError("Food quantity cannot be negative.")
                    device.food_quantity = new_food_quantity

                elif type == 'water':
                    new_water_quantity = device.water_quantity - quantity
                    if new_water_quantity < 0:
                        raise ValidationError("Water quantity cannot be negative.")
                    device.water_quantity = new_water_quantity

            # Save the updated device
            device.save()

            # Create a UsageLog entry
            usage_log = UsageLog.objects.create(
                device=device,
                log_type=f"{action}_{type}",
                quantity=quantity,
                time=timezone.now(),
                duration=None  # Assuming you calculate duration if needed
            )

            # TODO: Create a Notification entry
            #notification = Notification.objects.create(
            #    user=device.pet.user,
            #    notification_type="usage_log_created",
            #    message=f"{action.capitalize()} operation successful and usage log created."
            #)

            # Return the updated quantities and success message
            return Response({
                "food_quantity": device.food_quantity,
                "water_quantity": device.water_quantity,
                "message": f"{action.capitalize()} operation successful and usage log created."
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)