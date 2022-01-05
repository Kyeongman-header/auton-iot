from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings


class Machine(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.SET_DEFAULT,blank=True,null=True,default=None)
    id=models.CharField(primary_key=True,max_length=200)
    car_number=models.CharField(max_length=20,blank=True,null=True)
    pub_date=models.DateTimeField(default=timezone.localtime)

    def __str__(self):
        return str(self.id)
    
class GPS(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    gps=models.PointField()
    pub_date=models.DateTimeField(default=timezone.localtime,null=True)
    
    def __str__(self):
        return str(self.gps)
        
class QR(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    raw_id=models.CharField(max_length=200,null=True,blank=True)
    qr=models.URLField()
    
    pub_date=models.DateTimeField(default=timezone.localtime)
    
    def __str__(self):
        return str(self.qr)

class UserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        user=self.model(
                username=username,
                last_login=timezone.localtime(),
                date_joined=timezone.localtime(),
                **extra_fields
                )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username,password,**extra_fields):
        user=self.create_user(username,password=password,**extra_fields)
        user.is_admin=True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser, PermissionsMixin):
    #machine=models.CharField(max_length=20,unique=True)
    #machine=models.ForeignKey(Machine,on_delete=models.SET_DEFAULT,blank=True,null=True,default=None)
    username=models.CharField(primary_key=True,max_length=20,unique=True)
    
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.localtime)
    objects=UserManager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['password']

    def __str__(self):
        return self.username
    def has_perm(self,perm,obj=None):
        for p in self.get_all_permissions():
            if p == perm:
                return True
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    @property
    def is_staff(self):
        return self.is_admin


class Sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    sensor=models.JSONField()
    pub_date=models.DateTimeField('sensor date published',default=timezone.localtime)
    def __str__(self):
        return str(self.sensor)

class AirKorea(models.Model):
    machine=models.ForeignKey(Machine, on_delete=models.CASCADE)
    airkorea=models.JSONField()
    pub_date=models.DateTimeField('airkorea date published',default=timezone.localtime)
    def __str__(self):
        return str(self.airkorea)
    
class Hours_sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('hours date published',default=timezone.localtime)
    hours=models.FloatField(defalut=0,null=True, blank=True)
    hours_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.hours)
class Days_sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('days date published',default=timezone.localtime)
    days=models.FloatField(defalut=0,null=True, blank=True)
    days_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.days)
class Weeks_sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('weeks date published',default=timezone.localtime)
    weeks=models.FloatField(defalut=0,null=True, blank=True)
    weeks_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.weeks)
    
class Hours_airkorea(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('hours date published',default=timezone.localtime)
    hours=models.FloatField(defalut=0,null=True, blank=True)
    hours_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.hours)
class Days_airkorea(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('days date published',default=timezone.localtime)
    days=models.FloatField(defalut=0,null=True, blank=True)
    days_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.days)
class Weeks_airkorea(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    pub_date=models.DateTimeField('weeks date published',default=timezone.localtime)
    weeks=models.FloatField(defalut=0,null=True, blank=True)
    weeks_worst=models.FloatField(defalut=0)
    number=models.IntegerField(default=1)
    def __str__(self):
        return str(self.weeks)
