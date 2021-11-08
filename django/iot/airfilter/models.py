from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now

class Machine(models.Model):
    id=models.BigIntegerField(primary_key=True)
    car_number=models.CharField(max_length=20)
    pub_date=models.DateTimeField(default=now) 
    def __str__(self):
        return str(self.id)

class Sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    sensor=models.FloatField()
    pub_date=models.DateTimeField('sensor date published',default=now)
    def __str__(self):
        return str(self.sensor)

class AirKorea(models.Model):
    machine=models.ForeignKey(Machine, on_delete=models.CASCADE)
    airkorea=models.FloatField(max_length=100)
    pub_date=models.DateTimeField('airkor date published',default=now)
    def __str__(self):
        return str(self.airkorea)

class Seven_Days(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    seven_days_sensor=ArrayField(models.FloatField(),size=2)
    seven_days_airkorea=ArrayField(models.FloatField(),size=2)
    pub_date=models.DateTimeField('Seven days data published',default=now)
    def get_seven_days_sensor(self):
        return self.seven_days_sensor
    def get_seven_days_airkorea(self):
        return self.seven_days_airkorea

class Thirty_Days(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    thirty_days_sensor=ArrayField(ArrayField(models.FloatField(),size=31),size=2)
    thirty_days_airkorea=ArrayField(ArrayField(models.FloatField(),size=31),size=2)
    pub_date=models.DateTimeField('Thirty days data published',default=now)
    def get_thirty_days_sensor(self):
        return self.thirty_days_sensor
    def get_thirty_days_airkorea(self):
        return self.thirty_days_airkorea
