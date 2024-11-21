from rest_framework import serializers
from .models import (
    User, Role, UserDetails, Pet, Notification,
    Subscription, Payment, Device, UsageLog, Habit
)

# IAM
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), write_only=True, source='role'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'role_id', 'first_name', 'last_name']


# Profiles
class UserDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = UserDetails
        fields = ['id', 'user', 'user_id', 'first_name', 'last_name', 'birth_date', 'phone_number', 'image_url']


# Pets
class PetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = Pet
        fields = ['id', 'user', 'user_id', 'name', 'breed', 'species', 'birth_date', 'weight', 'age', 'image_url']


# Communications
class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = Notification
        fields = ['id', 'user', 'user_id', 'notification_type', 'message', 'created_at']


# Subscriptions & Billing
class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_id', 'plan_type', 'start_date', 'end_date', 'status']


class PaymentSerializer(serializers.ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    subscription_id = serializers.PrimaryKeyRelatedField(
        queryset=Subscription.objects.all(), write_only=True, source='subscription'
    )

    class Meta:
        model = Payment
        fields = ['id', 'subscription', 'subscription_id', 'amount', 'payment_date', 'payment_method', 'currency']


# Tracking
class DeviceSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(), write_only=True, source='pet'
    )

    class Meta:
        model = Device
        fields = ['id', 'pet', 'pet_id', 'serial_number', 'status', 'food_quantity', 'water_quantity', 'battery_quantity', 'food_limit', 'water_limit']


class UsageLogSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(read_only=True)
    device_id = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all(), write_only=True, source='device'
    )

    class Meta:
        model = UsageLog
        fields = ['id', 'device', 'device_id', 'log_type', 'quantity', 'time', 'duration']


class HabitSerializer(serializers.ModelSerializer):
    pet = PetSerializer(read_only=True)
    pet_id = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(), write_only=True, source='pet'
    )

    class Meta:
        model = Habit
        fields = ['id', 'pet', 'pet_id', 'water_consumption', 'food_consumption', 'start_date', 'end_date']


# custom serializers:

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(max_length=50)  # Accept the role name as a string
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    birth_date = serializers.DateField()
    phone_number = serializers.CharField(max_length=15)
    image_url = serializers.URLField(required=False, allow_blank=True)

    def validate_role(self, value):
        """Ensure the role is valid and exists in the database"""
        try:
            return Role.objects.get(name=value)  # Retrieve the Role based on name
        except Role.DoesNotExist:
            raise serializers.ValidationError("Role with the specified name does not exist.")
    
    def create(self, validated_data):
        # Extract user and user details data
        user_data = {key: validated_data[key] for key in ['username', 'email', 'password', 'role']}
        user_details_data = {key: validated_data[key] for key in ['first_name', 'last_name', 'birth_date', 'phone_number', 'image_url']}
        
        # Create the user instance
        user = User.objects.create_user(**user_data)
        
        # Create user details instance
        user_details = UserDetails.objects.create(user=user, **user_details_data)
        
        return user