from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomRateView, DiscountView, DiscountRoomRateView, OverridenRoomRateView, RoomRateAPIView, LivenessProbeView

router = DefaultRouter()
router.register(r'room_rates', RoomRateView)
router.register(r'discounts', DiscountView)
router.register(r'discountroom_rates', DiscountRoomRateView)
router.register(r'overriddenroom_rates', OverridenRoomRateView)

urlpatterns = [
  path('', include(router.urls)),
  path('final_rate', RoomRateAPIView.as_view(), name="room-rate-api)"),
  path('alive', LivenessProbeView.as_view(), name="liveliness-probe")
]
