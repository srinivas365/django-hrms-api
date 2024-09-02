from django.db import models

# Create your models here.
class RoomRate(models.Model):
  room_id = models.AutoField(primary_key=True)
  room_name = models.CharField(unique=True, max_length=200)
  default_rate = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"[{self.room_name}, {self.default_rate}]"
  
  
class OverriddenRoomRate(models.Model):
  room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE, related_name="overridden_rates")
  overridden_rate = models.DecimalField(max_digits=10, decimal_places=2)
  stay_date = models.DateField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  def __str__(self):
    return f"[{self.room_rate}, {self.stay_date}, {self.overridden_rate}]"

  
class Discount(models.Model):
  DISCOUNT_TYPE_CHOICES = [('fixed', 'fixed'), ('percentage', 'percentage')]
  
  discount_id = models.AutoField(primary_key=True)
  discount_name = models.CharField(unique=True, max_length=200)
  discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES)
  discount_value = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return f"[{self.discount_name}, {self.discount_type}, {self.discount_value}]"
  
class DiscountRoomRate(models.Model):
  room_rate = models.ForeignKey(RoomRate, on_delete=models.CASCADE, related_name="discounted_roomrates")
  discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name="discounted_rooms")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self) -> str:
    return f"{self.room_rate} - {self.discount}"
