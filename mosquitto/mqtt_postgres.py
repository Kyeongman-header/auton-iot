import paho.mqtt.client as mqtt
import psycopg2 as pg2
import datetime

import json

# import requests
# URL='https://auton-iot.com/'
# Token=''

HOST='localhost'
USER='user'
PASSWORD='1234'
PORT=8883
TOPIC='auton'
QOS=1

DB_HOST='10.0.10.161'
DB='iot'
DB_USER='auton'
DB_PASSWORD='mypassword'

def postgres_machine_add(host,user,password,db,car_number,machine_id):
    try:
        conn=pg2.connect(host=host,dbname=db,user=user,password=password)
    except Exception as e:
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            log.write("-----------------\n postgre sql connection error :( \n ---------------------")
            log.write(e)
        return
    cur=conn.cursor()
    query=f"INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES ({machine_id}, {car_number},current_timestamp)"
    try :
        cur.execute("INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES (%s, %s,current_timestamp)",(machine_id,car_number))
        conn.commit()
    except pg2.DatabaseError as dberror:
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            log.write("-----------------------\m insert query to machine table error :(\n ----------------------")
            log.write(dberror)
            conn.rollback()
    else :
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            log.write("insert success")
            log.write(query)
            
    conn.close()

def postgres_sensor_insert(host,user,password,db,sensor,machine_id):
    try:
        conn=pg2.connect(host=host,dbname=db,user=user,password=password)
    except Exception as e:
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
                log.write("-----------------\npostgre sql connection error :(\n--------------------")
                log.write(e)
        return

    cur=conn.cursor()
    n=datetime.datetime.now()
    query=f"INSERT INTO airfilter_sensor (machine_id,sensor,pub_date) VALUES ('{machine_id}', '{sensor}',current_timestamp)"
    
    try :
        cur.execute("INSERT INTO airfilter_sensor (machine_id,sensor,pub_date) VALUES (%s, %s, current_timestamp)",(machine_id,sensor))
        conn.commit()
    except pg2.DatabaseError as dberror:
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            log.write("------------------------\ninsert query to sensor table error :(\n-----------------------")
            log.write(dberror)
            conn.rollback()
    else :
        with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
            log.write("insert success : ")
            log.write(query)

    conn.close()


def on_connect(client,userdata,flags,rc):
    with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
        if rc == 0:
            log.write("Broker connected\n")
            #data={'user': 'mqtt_server','password':'ahtmzlxh1234'}
            #POST 방식, JSON은 아님.
            #res=requests.post(URL+'api-token-auth/',data=data)
            #if res.status_code == 200 :
            #    Token=res.json()["token"]
            #    log.write(" REST server login success.\n")
            #else :
            #    log.write(str(res.status_code) + " REST server login error\n")
            #    log.write(res.text + '\n')

        else:
            log.write("Broker connection failure : " + str(rc))
        log.write(str(datetime.datetime.now()) + '\n')
    

def on_disconnect(client, userdata, flags, rc=0):
    with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
        log.write("disconnection success. "+str(flags)+ "result code : " + str(rc) + '\n')
        log.write(str(datetime.datetime.now()) + '\n')
        log.close()
            


def on_subscribe(client,userdata,mid,granted_qos):
    with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
        log.write("subscribed : " + TOPIC + " qos : "+ str(granted_qos) + '\n')
        log.write(str(datetime.datetime.now()) + '\n')

def on_message(client,userdata,msg):
    
    # 실제로는 json data로 받고 sensor와 car_number를 더 쉽게 파싱할 수 있음.
    # 지금은 0 번째 숫자로 추가인지 아닌지 가리고, 1,2번째 숫자가 sensor값(혹은 차 넘버),
    #3번째 숫자가 machine 고유 번호임.
    with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
        data=str(msg.payload.decode("utf-8"))
        # data='{ "is_add" : 1 , "machine" : 55 , "car_number" : "12허 1234", "sensor" : {"Temp" : 21.0, "CO2" : 10.5 , "NO2" : 53.2 } }'
        j=json.loads(data)
        is_add=j["is_add"]
        sensor=j["sensor"]
        machine_id=j["machine"]
        car_number=j["car_number"]
        #token='Token ' + Token
        #headers={'Authorization' : token}
        
        if is_add=='1':
            log.write("is_add : " + is_add + " car_number : " + car_number + " machine_id : " + machine_id + '\n')
            postgres_machine_add(DB_HOST,DB_USER,DB_PASSWORD,DB,car_number,machine_id)
#             data={ "id" : int(machine_id), "car_number" : sensor_or_car_number }
#             res=requests.post(URL+'api/machine/',headers=headers,data=data)
#             if res.status_code ==201:
#                 log.write( str(res.status_code) + " successfully add machine " + machine_id + " " + str(res.json()["pub_date"]) + '\n')
#             else :
#                 log.write( str(res.status_code) + " error add machine. " + machine_id + '\n')
#                 log.write( res.text + '\n' )

        else :
            log.write("is_add : " + is_add + " sensor : " + json.dumps(sensor) + " machine_id : " + machine_id + '\n')
            postgres_sensor_insert(DB_HOST,DB_USER,DB_PASSWORD,DB,json.dumps(sensor),machine_id)
#             data={ "machine" : int(machine_id), "sensor" : int(sensor_or_car_number) }
#             res=requests.post(URL+'api/sensor/',headers=headers,data=data)
#             if res.status_code == 201:
#                 log.write( str(res.status_code) + "successfully updating sensor data. " + machine_id + " " + str(res.json()["pub_date"]) + '\n')
#             else :
#                 log.write( str(res.status_code) + "error updating sensor data. " + machine_id + '\n')
#                 log.write( res.text + '\n')
           
    
        log.write(str(datetime.datetime.now()) + '\n')

            
client=mqtt.Client()
client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_subscribe=on_subscribe
client.on_message=on_message

client.username_pw_set(username=USER,password=PASSWORD)

client.connect(HOST,PORT)
client.subscribe(TOPIC,QOS)

rc=0
while rc == 0:
    rc = client.loop()
    
with open("/home/ubuntu/mqtt_postgres.log",'a') as log :
    log.write("end of python code.\n")
    log.write(str(datetime.datetime.now()) + '\n')
    log.close()
