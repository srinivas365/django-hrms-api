from .models import RoomRate, OverriddenRoomRate, DiscountRoomRate
def get_final_rate(room_id, date):
  try:
    room_rate = RoomRate.objects.get(room_id=room_id)
    
    # fetching the overridden rate if present
    overridden_rate = OverriddenRoomRate.objects.filter(
      room_rate=room_rate,
      stay_date=date
    ).values('overridden_rate').first()
    final_rate = overridden_rate['overridden_rate'] if overridden_rate else room_rate.default_rate
    
    # fetching all the discounts for the room
    discounts = DiscountRoomRate.objects.filter(room_rate=room_rate).select_related('discount')
    
    # calculating the final_rate
    discounted_rates = [final_rate]
    for discountObj in discounts:
      if discountObj.discount.discount_type == 'percentage':
        discounted_rates.append(room_rate.default_rate * discountObj.discount.discount_value * 1/100)
      else:
        discounted_rates.append(room_rate.default_rate - discountObj.discount.discount_value)
    return min(discounted_rates)
  except RoomRate.DoesNotExist:
    return None