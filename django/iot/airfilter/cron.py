from .models import *
from django.db.models import Avg, Max
import datetime

now=datetime.datetime.now()

def seven_days(id):
    m=Machine.objects.get(id=id)

    i=7
    m.seven_days_set.delete()
    while i > 0 :
        sensors=m.sensor_set.filter(pub_date__day=(now.day-datetime.timedelta(days=i)))
        airkoreas=m.airkorea_set.filter(pub_date__day=(now.day-datetime.timedelta(days=i)))
        m.seven_days_set.create(seven_days_sensor=[sensors.aggregate(Avg('sensor')),sensors.aggregate(Max('sensor'))],seven_days_airkorea=[airkoreas.aggregate(Avg('airkorea')),airkoreas.aggregate(Max('airkorea'))],pub_date=now)
        



 
def thirty_days(id):
    m=Machine.objects.get(id=id)

    i=4
    m.thirty_days_set.delete()
    while i>0 :
        sensors=m.sensor_set.filter(pub_date__gte=(now-datetime.timedelta(weeks=i)),pub_date__lte=(now-datetime.timedelta(weeks=i-1)))
        airkoreas=m.airkorea_set.filter(pub_date__da=(now-datetime.timedelta(weeks=i)),pub_date_lte=(now-datetime.timedelta(weeks=i-1)))

        m.thirty_days_set.create(thirty_days_sensor=[sensors.aggregate(Avg('sensor')),sensors.aggregate(Max('sensor'))],thirty_days_airkorea=[airkoreas.aggregate(Avg('airkorea')),airkoreas.aggregate(Max('airkorea'))],pub_date=now)


