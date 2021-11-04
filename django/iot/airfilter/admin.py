from django.contrib import admin
from .models import *

# Register your models here.

class SensorInline(admin.TabularInline):
    model=Machine
    extra=3

class MachineAdmin(admin.ModelAdmin):
    readonly_fields=('id',)
    list_display=('id','car_number','pub_date')
    list_filter=['pub_date']
    search_fields=['id','car_number']

admin.site.register(Machine,MachineAdmin)
admin.site.register(Sensor)
admin.site.register(AirKorea)
admin.site.register(Seven_Days)
admin.site.register(Thirty_Days)
