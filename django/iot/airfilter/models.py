from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,app,machine=None,password=None):
        user=self.model(
                app=app,
                machine=machine
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,app,password):
        user=self.create_user(app,password=password)
        user.is_admin=True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE,blank=True,null=True)
    app=models.CharField(max_length=20,unique=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)

    objects=UserManager()
    USERNAME_FIELD='app'
    REQUIRED_FIELDS=['machine','password']

    def __str__(self):
        return self.app
    def has_perm(self,perm,obj=None):
        return True
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin




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
    seven_days_sensor_avg=models.FloatField(blank=True,null=True)
    seven_days_sensor_max=models.FloatField(blank=True,null=True)
    seven_days_airkorea_avg=models.FloatField(blank=True,null=True)
    seven_days_airkorea_max=models.FloatField(blank=True,null=True)
    pub_date=models.DateTimeField('Seven days data published',default=now)

class Thirty_Days(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    thirty_days_sensor_avg=models.FloatField(blank=True,null=True)
    thirty_days_sensor_max=models.FloatField(blank=True,null=True)
    thirty_days_airkorea_avg=models.FloatField(blank=True,null=True)
    thirty_days_airkorea_max=models.FloatField(blank=True,null=True)
    pub_date=models.DateTimeField('Thirty days data published',default=now)
