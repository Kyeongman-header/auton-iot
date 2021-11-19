from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm,UserCreationForm
from .models import *

# Register your models here.

# class SensorInline(admin.TabularInline):
#     model=Machine
#     extra=3


class UserAdmin(BaseUserAdmin):
    form=UserChangeForm
    add_form=UserCreationForm

    list_display=('username','is_admin')
    list_filter=('is_admin',)
    fieldsets=(
            (None,{'fields':('username','password')}),
            (('Permissions'),{'fields':('is_admin','user_permissions')}),
            (('Important dates'), {'fields': ('last_login', 'date_joined')} ),
            )
    add_fieldsets=(
            (None,{
                'classes':('wide',),
                'fields':('username','password1','password2')}
                ),
            )
    search_fields=('username',)
    ordering=('username',)
    filter_horizontal=()

class MachineAdmin(admin.ModelAdmin):
    list_display=('id','car_number','pub_date')
    list_filter=['id','car_number','pub_date']
    search_fields=['id','car_number','pub_date']
class GPSAdmin(OSMGeoAdmin):
    list_display=('pub_date','gps','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','gps']
class QRAdmin(admin.ModelAdmin):
    list_display=('pub_date','qr','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','qr']
class SensorAdmin(admin.ModelAdmin):
    list_display=('pub_date','sensor','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','sensor']

class AirKoreaAdmin(admin.ModelAdmin):
    list_display=('pub_date','airkorea','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','sensor']
    
class SevenDaysAdmin(admin.ModelAdmin):
    list_display=('pub_date','seven_days_sensor_avg','seven_days_sensor_max','seven_days_airkorea_avg','seven_days_airkorea_max','machine')
    list_filter=['machine']
    search_fields=['machine']
    
class ThirtyDaysAdmin(admin.ModelAdmin):
    list_display=('pub_date','thirty_days_sensor_avg','thirty_days_sensor_max','thirty_days_airkorea_avg','thirty_days_airkorea_max','machine')
    list_filter=['machine']
    search_fields=['machine']
    
admin.site.register(GPS,GPSAdmin)    
admin.site.register(QR,QRAdmin)
admin.site.register(MyUser,UserAdmin)
admin.site.unregister(Group)
admin.site.register(Machine,MachineAdmin)
admin.site.register(Sensor,SensorAdmin)
admin.site.register(AirKorea,AirKoreaAdmin)
admin.site.register(Seven_Days,SevenDaysAdmin)
admin.site.register(Thirty_Days,ThirtyDaysAdmin)
