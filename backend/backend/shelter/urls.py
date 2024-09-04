from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AnimalViewSet, AdoptionViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'animals', AnimalViewSet)
router.register(r'adoptions', AdoptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
