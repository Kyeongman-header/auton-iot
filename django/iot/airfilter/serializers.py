from .models import *
from rest_framework import serializers

class HoursSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hours_sensor
        fields=['machine','hours','pub_date']

class DaysSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Days_sensor
        fields=['machine','days','pub_date']

class WeeksSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Weeks_sensor
        fields=['machine','weeks','pub_date']
        
class HoursSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hours_airkorea
        fields=['machine','hours','pub_date']

class DaysSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Days_airkorea
        fields=['machine','days','pub_date']

class WeeksSensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Weeks_airkorea
        fields=['machine','weeks','pub_date'] 
        
class GPSSerializer(serializers.ModelSerializer):
    class Meta:
        model=GPS
        fields=['machine','gps','pub_date']
class QRSerializer(serializers.ModelSerializer):
    class Meta:
        model=QR
        fields=['machine','qr','raw_id','pub_date']       
class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields=['username','password','last_login']
class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sensor
        fields=['machine','sensor','pub_date']
        
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model=Machine
        fields=['id','car_number','pub_date','user']
        
class AirKoreaSerializer(serializers.ModelSerializer):
    class Meta:
        model=AirKorea
        fields=['machine','airkorea','pub_date']
        
# class SevenDaysSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Seven_Days
#         fields=['machine','seven_days_sensor_avg','seven_days_sensor_max','seven_days_airkorea_avg','seven_days_airkorea_max','pub_date']
        
# class ThirtyDaysSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Thirty_Days
#         fields=['machine','thirty_days_sensor_avg','thirty_days_sensor_max','thirty_days_airkorea_avg','thirty_days_airkorea_max','pub_date']
        
