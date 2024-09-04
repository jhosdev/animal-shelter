from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Adoption

@receiver(post_delete, sender=Adoption)
def set_animal_available(sender, instance, **kwargs):
    print('set_animal_available')
    animal = instance.animal
    if animal is not None:
        animal.status = 'AVAILABLE'
        animal.save()