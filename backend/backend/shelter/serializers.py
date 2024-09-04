from django.template.context_processors import request
from rest_framework import serializers
from .models import User, Animal, Adoption


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'status']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'ADOPTER'),  # Default role is ADOPTER
            status=validated_data.get('status', 'ACTIVE')
        )
        return user


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = '__all__'
        extra_kwargs = {
            'volunteer': {'required': False},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        validated_data['volunteer'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        if 'status' in validated_data:
            if validated_data['status'] == 'PENDING':
                Adoption.objects.create(
                    animal=instance,
                    adopter=user,
                    volunteer=user,
                    status=validated_data['status']
                )
            if validated_data['status'] == 'ADOPTED':
                adoption, created = Adoption.objects.get_or_create(
                    animal=instance,
                    defaults={
                        'adopter': user,
                        'volunteer': user,
                        'status': 'COMPLETED'
                    }
                )
                if not created:
                    if adoption.status == 'PENDING':
                        adoption.status = 'COMPLETED'
                        adoption.save()

        return super().update(instance, validated_data)


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = '__all__'
        extra_kwargs = {
            'adopter': {'required': False},
            'volunteer': {'required': False},
        }

    def create(self, validated_data):
        animal_id = self.context['request'].data.get('animal')
        animal = Animal.objects.get(id=animal_id)

        if animal is None:
            raise serializers.ValidationError("Invalid animal ID.")

        if animal.status != 'AVAILABLE':
            raise serializers.ValidationError("Animal is not available.")

        user = self.context['request'].user
        validated_data['adopter'] = user
        validated_data['volunteer'] = animal.volunteer

        animal.status = 'PENDING'
        animal.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):

        animal = instance.animal

        if 'animal' in validated_data:
            animal_id = validated_data['animal']
            animal = Animal.objects.get(id=animal_id)

        if 'status' in validated_data:
            if validated_data['status'] == 'COMPLETED':
                animal.status = 'ADOPTED'
            elif validated_data['status'] == 'CANCELLED':
                animal.status = 'AVAILABLE'

            animal.save()

        return super().update(instance, validated_data)
