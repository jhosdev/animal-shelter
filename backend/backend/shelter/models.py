import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# IAM
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, related_name='users')
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        return self.username


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Profiles
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='details')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    phone_number = models.CharField(max_length=15)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# Pets
class Pet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    species = models.CharField(max_length=50)  # For example, "Dog", "Cat"
    birth_date = models.DateField()
    weight = models.FloatField()
    age = models.IntegerField()
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


# Communications
class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification to {self.user} - {self.notification_type}'


# Subscriptions & Billing
class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.plan_type} - {self.status}'


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=50)
    currency = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.amount} {self.currency} - {self.payment_date}'


# Tracking
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='devices')
    serial_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.serial_number


class UsageLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='usage_logs')
    log_type = models.CharField(max_length=50)
    quantity = models.FloatField()
    time = models.DateTimeField()
    duration = models.DurationField()  # Stored as a timedelta

    def __str__(self):
        return f'{self.log_type} at {self.time}'


class Habit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='habits')
    water_consumption = models.FloatField()
    food_consumption = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'Habit for {self.pet.name}'
