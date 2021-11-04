from django.db import models
from django.utils.timezone import now

class Machine(models.Model):
    id=models.BigIntegerField(primary_key=True)
    car_number=models.CharField(max_length=20)
    pub_date=models.DateTimeField(default=now) 
    def __str__(self):
        return str(self.id)

class Sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    sensor=models.CharField(max_length=100)
    pub_date=models.DateTimeField('sensor date published')
    def __str__(self):
        return self.sensor

class AirKorea(models.Model):
    machine=models.ForeignKey(Machine, on_delete=models.CASCADE)
    airkorea=models.CharField(max_length=100)
    pub_date=models.DateTimeField('airkor date published')
    def __str__(self):
        return self.airkorea

class Seven_Days(models.Model):
    machine=models.CharField(max_length=100)
    seven_days_sensor=models.CharField(max_length=100)
    seven_days_airkorea=models.CharField(max_length=100)
    def get_seven_days_sensor(self):
        return self.seven_days_sensor
    def get_seven_days_airkorea(self):
        return self.seven_days_airkorea

class Thirty_Days(models.Model):
    machine=models.CharField(max_length=100)
    thirty_days_sensor=models.CharField(max_length=100)
    thirty_days_airkorea=models.CharField(max_length=100)
    def get_thirty_days_sensor(self):
        return self.thirty_days_sensor
    def get_thirty_days_airkorea(self):
        return self.thirty_days_airkorea
