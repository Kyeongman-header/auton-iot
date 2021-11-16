from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.timezone import now
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.conf import settings


content_type = ContentType.objects.get_for_model()
permission = Permission.objects.create(
    codename='can_publish',
    name='Can Publish Posts',
    content_type=content_type,
)

class Machine(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_DEFAULT,blank=True,null=True,default=None)
    id=models.BigIntegerField(primary_key=True)
    car_number=models.CharField(max_length=20)
    pub_date=models.DateTimeField(default=now) 
    def __str__(self):
        return str(self.id)


class UserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        user=self.model(
                username=username,
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
    #machine=models.ForeignKey(Machine,on_delete=models.CASCADE,blank=True,null=True)
    username=models.CharField(max_length=20,unique=True)
    
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
    objects=UserManager()
    USERNAME_FIELD='username'
    REQUIRED_FIELDS=['password']

    def __str__(self):
        return self.username
#     def has_perm(self,perm,obj=None):
#         return True
#     def has_module_perms(self,app_label):
#         return True
    @property
    def is_staff(self):
        return self.is_admin


class Sensor(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    sensor=models.JSONField()
    pub_date=models.DateTimeField('sensor date published',default=now)
    def __str__(self):
        return str(self.sensor)

class AirKorea(models.Model):
    machine=models.ForeignKey(Machine, on_delete=models.CASCADE)
    airkorea=models.JSONField()
    pub_date=models.DateTimeField('airkor date published',default=now)
    def __str__(self):
        return str(self.airkorea)

class Seven_Days(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    seven_days_sensor_avg=models.JSONField(blank=True,null=True)
    seven_days_sensor_max=models.JSONField(blank=True,null=True)
    seven_days_airkorea_avg=models.JSONField(blank=True,null=True)
    seven_days_airkorea_max=models.JSONField(blank=True,null=True)
    pub_date=models.DateTimeField('Seven days data published',default=now)

class Thirty_Days(models.Model):
    machine=models.ForeignKey(Machine,on_delete=models.CASCADE)
    thirty_days_sensor_avg=models.JSONField(blank=True,null=True)
    thirty_days_sensor_max=models.JSONField(blank=True,null=True)
    thirty_days_airkorea_avg=models.JSONField(blank=True,null=True)
    thirty_days_airkorea_max=models.JSONField(blank=True,null=True)
    pub_date=models.DateTimeField('Thirty days data published',default=now)
