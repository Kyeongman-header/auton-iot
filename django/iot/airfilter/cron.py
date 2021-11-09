from .models import *
from django.db.models import Avg, Max
import datetime



def seven_thirty_days():
    print("test")
    m_all=Machine.objects.all()
    now=datetime.datetime.now()
    for i in m_all:
        ID=i.id
        print(f"cron job for {ID} machine. {now} \n")
        seven_days(ID)
        thirty_days(ID)


def seven_days(id):
    now=datetime.datetime.now()
    m=Machine.objects.get(id=id)

    i=7
    if m.seven_days_set.count()!=0 :
        m.seven_days_set.all().delete()
        print(f"seven_days table clearing job success.\n")
    while i > 0 :
        sensors=m.sensor_set.filter(pub_date__gte=(now-datetime.timedelta(days=i)),pub_date__lte=(now-datetime.timedelta(days=i-1))).all()
        airkoreas=m.airkorea_set.filter(pub_date__gte=(now-datetime.timedelta(days=i)),pub_date__lte=(now-datetime.timedelta(days=i-1))).all()
        i=i-1
        if sensors.count()==0 or airkoreas.count() == 0:
            m.seven_days_set.create(pub_date=now)
            m.save()
            print(f"seven_days_cron : {i} day does not exists\n")
            continue
        avg_sensor=sensors.aggregate(Avg('sensor'))['sensor__avg']
        max_sensor=sensors.aggregate(Max('sensor'))['sensor__max']
        avg_airkorea=airkoreas.aggregate(Avg('airkorea'))['airkorea__avg']
        max_airkorea=airkoreas.aggregate(Max('airkorea'))['airkorea__max']

        m.seven_days_set.create(seven_days_sensor_avg=avg_sensor,seven_days_sensor_max=max_sensor,seven_days_airkorea_avg=avg_airkorea,seven_days_airkorea_max=max_airkorea,pub_date=sensors.first().pub_date)
        m.save()
        print(f"seven_days_cron : {i} day, data stored successfully on {now}\n")



 
def thirty_days(id):
    now=datetime.datetime.now()
    m=Machine.objects.get(id=id)

    i=4
    if m.thirty_days_set.count()!=0 :
        m.thirty_days_set.all().delete()
        print(f"thirty_days table clearing job success. \n")
    while i>0 :
        sensors=m.sensor_set.filter(pub_date__gte=(now-datetime.timedelta(weeks=i)),pub_date__lte=(now-datetime.timedelta(weeks=i-1))).all()
        airkoreas=m.airkorea_set.filter(pub_date__gte=(now-datetime.timedelta(weeks=i)),pub_date__lte=(now-datetime.timedelta(weeks=i-1))).all()

        i=i-1
        if sensors.count()==0 or airkoreas.count()==0 :
            m.thirty_days_set.create(pub_date=now)
            m.save()
            print(f"thirty_days_cron : {i} week does not exists.\n")
            continue
        avg_sensor=sensors.aggregate(Avg('sensor'))['sensor__avg']
        avg_airkorea=airkoreas.aggregate(Avg('airkorea'))['airkorea__avg']
        Max_sensor=sensors.aggregate(Max('sensor'))['sensor__max']
        Max_airkorea=airkoreas.aggregate(Max('airkorea'))['airkorea__max']
        m.thirty_days_set.create(thirty_days_sensor_avg=avg_sensor,thirty_days_sensor_max=Max_sensor,thirty_days_airkorea_avg=avg_airkorea,thirty_days_airkorea_max=Max_airkorea,pub_date=sensors.first().pub_date)
        m.save()
        print(f"thirty_days_cron : {i} week, data stored successfully on {now}\n") 


