from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from .views import (
    SignUpViewSet, UpdateDeviceQuantityViewSet, UserViewSet, RoleViewSet, UserDetailsViewSet, PetViewSet, NotificationViewSet,
    SubscriptionViewSet, PaymentViewSet, DeviceViewSet, UsageLogViewSet, HabitViewSet
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('roles', RoleViewSet)
router.register('user-details', UserDetailsViewSet)
router.register('pets', PetViewSet)
router.register('notifications', NotificationViewSet)
router.register('subscriptions', SubscriptionViewSet)
router.register('payments', PaymentViewSet)
router.register('devices', DeviceViewSet)
router.register('usage-logs', UsageLogViewSet)
router.register('habits', HabitViewSet)
router.register(r'update-device-quantity', UpdateDeviceQuantityViewSet, basename='update-device-quantity')


urlpatterns = router.urls


urlpatterns = [
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('signup/', SignUpViewSet.as_view({'post': 'create'}), name='signup'),
    path('', include(router.urls)),
]
