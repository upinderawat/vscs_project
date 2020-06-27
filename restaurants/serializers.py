from rest_framework import serializers
from .models import Reservation
class ReservationSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields= ['email','restaurant','numberOfPeople','time']