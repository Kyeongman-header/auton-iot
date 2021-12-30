from .models import *
from django.db.models import Avg, Max
import datetime
from .lists import sensor_list, airkorea_list
from django.db.models.functions import Cast
from django.db.models import FloatField
from django.contrib.postgres.fields.jsonb import KeyTextTransform


def deleter():
    now=datetime.datetime.now()
    
    #m_all=Machine.objects.filter(pub_date__lte=(now-datetime.timedelta(weeks=)) # 머신은 단순히 기간 종료가 있지는 않을듯.
    
    try :
        Sensor.objects.filter(pub_date__lte=(now-datetime.timedelta(weeks=4))).delete()
    except :
        print(f"Erro : deleting cron job : sensor. \n")
                        
    
    try :
        AirKorea.objects.filter(pub_date__lte=(now-datetime.timedelta(weeks=4))).delete()
    except:
        print(f"Erro : deleting cron job : airkorea. \n")
    try :
        GPS.objects.filter(pub_date__lte=(now-datetime.timedelta(weeks=4))).delete()
    except:
        print(f"Erro : deleting cron job : gps. \n")
    try :    
        MyUser.objects.filter(last_login__lte=(now-datetime.timedelta(weeks=4))).delete()
    except:
        print(f"Erro : deleting cron job : myuser. \n")
    
    

def seven_thirty_days():
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
            m.seven_days_set.create(pub_date=now-datetime.timedelta(days=i+1))
            m.save()
            print(f"seven_days_cron : {i} day does not exists\n")
            continue
        seven_days_sensor_avg_json={}
        seven_days_sensor_max_json={}
        seven_days_airkorea_avg_json={}
        seven_days_airkorea_max_json={}
        
        for s in sensor_list:
            avg_sensor=sensors.annotate(float_val=Cast(KeyTextTransform(s, 'sensor'),FloatField())).aggregate(Avg('float_val'))['float_val__avg']
            max_sensor=sensors.annotate(float_val=Cast(KeyTextTransform(s, 'sensor'),FloatField())).aggregate(Max('float_val'))['float_val__max']

            seven_days_sensor_avg_json[s] = avg_sensor
            seven_days_sensor_max_json[s] = max_sensor

        for a in airkorea_list:
            avg_airkorea=airkoreas.annotate(float_val=Cast(KeyTextTransform(a, 'airkorea'),FloatField())).aggregate(Avg('float_val'))['float_val__avg']
            max_airkorea=airkoreas.annotate(float_val=Cast(KeyTextTransform(a, 'airkorea'),FloatField())).aggregate(Max('float_val'))['float_val__max']
            
            seven_days_airkorea_avg_json[a] = avg_airkorea
            seven_days_airkorea_max_json[a] = max_airkorea
            
        m.seven_days_set.create(seven_days_sensor_avg=seven_days_sensor_avg_json,seven_days_sensor_max=seven_days_sensor_max_json,seven_days_airkorea_avg=seven_days_airkorea_avg_json,seven_days_airkorea_max=seven_days_airkorea_max_json,pub_date=sensors.first().pub_date)
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
            m.thirty_days_set.create(pub_date=now-datetime.timedelta(days=i+1))
            m.save()
            print(f"thirty_days_cron : {i} week does not exists.\n")
            continue
      
        thirty_days_sensor_avg_json={}
        thirty_days_sensor_max_json={}
        thirty_days_airkorea_avg_json={}
        thirty_days_airkorea_max_json={}
        
        for s in sensor_list:
            avg_sensor=sensors.annotate(float_val=Cast(KeyTextTransform(s, 'sensor'),FloatField())).aggregate(Avg('float_val'))['float_val__avg']
            max_sensor=sensors.annotate(float_val=Cast(KeyTextTransform(s, 'sensor'),FloatField())).aggregate(Max('float_val'))['float_val__max']
            thirty_days_sensor_avg_json[s] = avg_sensor
            thirty_days_sensor_max_json[s] = max_sensor
        for a in airkorea_list:
            avg_airkorea=airkoreas.annotate(float_val=Cast(KeyTextTransform(a, 'airkorea'),FloatField())).aggregate(Avg('float_val'))['float_val__avg']
            max_airkorea=airkoreas.annotate(float_val=Cast(KeyTextTransform(a, 'airkorea'),FloatField())).aggregate(Max('float_val'))['float_val__max']
            thirty_days_airkorea_avg_json[a] = avg_airkorea
            thirty_days_airkorea_max_json[a] = max_airkorea  
        
        m.thirty_days_set.create(thirty_days_sensor_avg=thirty_days_sensor_avg_json,thirty_days_sensor_max=thirty_days_sensor_max_json,thirty_days_airkorea_avg=thirty_days_airkorea_avg_json,thirty_days_airkorea_max=thirty_days_airkorea_max_json,pub_date=sensors.first().pub_date)
        
        m.save()
        print(f"thirty_days_cron : {i} week, data stored successfully on {now}\n") 


