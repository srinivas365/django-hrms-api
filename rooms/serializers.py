from rest_framework import serializers
from .models import RoomRate, Discount, DiscountRoomRate, OverriddenRoomRate

class RoomRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = RoomRate
    fields = "__all__"
    
class DiscountSerializer(serializers.ModelSerializer):
  class Meta:
    model = Discount
    fields = "__all__"
    
class DiscountRoomRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = DiscountRoomRate
    fields = "__all__"
    
class OverriddenRoomRateSerializer(serializers.ModelSerializer):
  class Meta:
    model = OverriddenRoomRate
    fields = "__all__"

  