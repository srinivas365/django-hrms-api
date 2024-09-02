from django.shortcuts import render
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from .models import Discount, DiscountRoomRate, RoomRate, OverriddenRoomRate
from .serializers import RoomRateSerializer, DiscountSerializer, DiscountRoomRateSerializer, OverriddenRoomRateSerializer
from datetime import datetime, timedelta
from .utils import get_final_rate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class LivenessProbeView(views.APIView):
  def get(self, request):
    return Response(status=status.HTTP_200_OK)
      
class RoomRateView(viewsets.ModelViewSet):
  queryset = RoomRate.objects.all()
  serializer_class = RoomRateSerializer
  
class DiscountView(viewsets.ModelViewSet):
  queryset = Discount.objects.all()
  serializer_class = DiscountSerializer
  
class DiscountRoomRateView(viewsets.ModelViewSet):
  queryset = DiscountRoomRate.objects.all()
  serializer_class = DiscountRoomRateSerializer
  
class OverridenRoomRateView(viewsets.ModelViewSet):
  queryset = OverriddenRoomRate.objects.all()
  serializer_class = OverriddenRoomRateSerializer
  
class RoomRateAPIView(views.APIView):
  @swagger_auto_schema(
    manual_parameters=[
      openapi.Parameter('room_id', openapi.IN_QUERY, description="Room ID", type=openapi.TYPE_STRING),
      openapi.Parameter('start_date', openapi.IN_QUERY, description="Check-in date", type=openapi.TYPE_STRING),
      openapi.Parameter('end_date', openapi.IN_QUERY, description="Check-out date", type=openapi.TYPE_STRING)
    ]
  )
  def get(self, request, *args, **kwargs):
    room_id = request.query_params.get('room_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    if not room_id or not start_date or not end_date:
      return Response({"msg": "room_id, start_date and end_date fields are missing"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
      room_id = int(room_id)
      start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
      end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
      
      if end_date < start_date:
        return Response({"detail": "end_date should be after start_date."}, status=status.HTTP_400_BAD_REQUEST)

      output = []
      final_price = 0
      current_date = start_date 
      while current_date <= end_date:
        final_rate = get_final_rate(room_id, current_date)
        if final_rate is not None:
          output.append({
              'room_id': room_id,
              'room_name': RoomRate.objects.get(room_id=room_id).room_name,
              'date': current_date,
              'final_rate': final_rate
          })
          final_price += final_rate 
          current_date += timedelta(days=1)
      
      return Response({ "prices": output, "final_price": final_price }, status=status.HTTP_200_OK)
    except RoomRate.DoesNotExist:
      return Response({"detail": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
      