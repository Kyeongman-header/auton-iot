from django.contrib import admin
from .models import *

# Register your models here.

# class SensorInline(admin.TabularInline):
#     model=Machine
#     extra=3

class MachineAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display=('id','car_number','pub_date')
    list_filter=['id','car_number','pub_date']
    search_fields=['id','car_number','pub_date']
    
class SensorAdmin(admin.ModelAdmin):
    list_display=('pub_date','sensor','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','sensor']

class AirKoreaAdmin(admin.ModelAdmin):
    list_display=('pub_date','airkorea','machine')
    list_filter=('machine','pub_date')
    search_fields=['machine','pub_date','sensor']
    
class SevenDaysAdmin(admin.ModelAdmin):
    list_display=('seven_days_sensor','seven_days_airkorea','machine')
    list_filter=['machine']
    search_fields=['machine']
    
class ThirtyDaysAdmin(admin.ModelAdmin):
    list_display=('thirty_days_sensor','thirty_days_airkorea','machine')
    list_filter=['machine']
    search_fields=['machine']

admin.site.register(Machine,MachineAdmin)
admin.site.register(Sensor,SensorAdmin)
admin.site.register(AirKorea,AirKoreaAdmin)
admin.site.register(Seven_Days,SevenDaysAdmin)
admin.site.register(Thirty_Days,ThirtyDaysAdmin)
