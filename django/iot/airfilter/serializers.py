from .models import *
from rest_framework import serializers

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sensor
        fields=['machine','sensor','pub_date']
        
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machine
        fields=['id','car_number','pub_date']
        
class AirKoreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=AirKorea
        fields=['machine','airkorea','pub_date']
        
class Seven_Days_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Seven_Days
        fields=['machine','seven_days_sensor','seven_days_airkorea']
        
class Thirty_Days_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Thirty_Days
        fields=['machine','thirty_days_sensor','thirty_days_airkorea']
        
