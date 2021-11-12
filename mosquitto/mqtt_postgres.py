import paho.mqtt.client as mqtt
import psycopg2 as pg2
import datetime

import json

import requests

log=open("/home/ubuntu/mqtt_postgres.log",'w')
URL='https://auton-iot.com/'
Token=''

HOST='localhost'
USER='user'
PASSWORD='1234'
PORT=8883
TOPIC='auton'
QOS=1

# DB_HOST='10.0.10.161'
# DB='iot'
# DB_USER='auton'
# DB_PASSWORD='mypassword'

# def postgres_machine_add(host,user,password,db,car_number,machine_id):
#     try:
#         conn=pg2.connect(host=host,dbname=db,user=user,password=password)
#     except Exception as e:
#         print("-----------------\n postgre sql connection error :( \n ---------------------")
#         print(e)
#         return
#     cur=conn.cursor()
#     query=f"INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES ({machine_id} {car_number},current_timestamp)"
#     try :
#         cur.execute("INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES (%s, %s,current_timestamp)",(machine_id,car_number))
#         conn.commit()
#     except pg2.DatabaseError as dberror:
#         print("-----------------------\m insert query to machine table error :(\n ----------------------")
#         print(dberror)
#         conn.rollback()
#     else :
#         print("insert success")
#         print(query)
#     conn.close()

# def postgres_sensor_insert(host,user,password,db,sensor,machine_id):
#     try:
#         conn=pg2.connect(host=host,dbname=db,user=user,password=password)
#     except Exception as e:
#         print("-----------------\npostgre sql connection error :(\n--------------------")
#         print(e)
#         return

#     cur=conn.cursor()
#     n=datetime.datetime.now()
#     query=f"INSERT INTO airfilter_sensor VALUES ('{sensor}','{n}','{machine_id}')"
    
#     try :
#         cur.execute("INSERT INTO airfilter_sensor (machine_id,sensor,pub_date)VALUES (%s, %s, current_timestamp)",(machine_id,sensor))
#         conn.commit()
#     except pg2.DatabaseError as dberror:
#         print("------------------------\ninsert query to sensor table error :(\n-----------------------")
#         print(dberror)
#         conn.rollback()
#     else :
#         print("insert success : ")
#         print(query)

#     conn.close()


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        log.write("Broker connected")
        data={'user': 'mqtt_server','password':'ahtmzlxh1234'}
        #POST 방식, JSON은 아님.
        res=requests.get(URL+'rest-auth/api-token-auth/',data=data)
        if res.status_code == 200 :
            Token=res.json()["token"]
            log.write(" REST server login success.\n")
        else :
            log.write(str(res.status_code) + " REST server login error")
            log.write(res.text)
        
    else:
        log.write("Broker connection failure : " + str(rc))
    

def on_disconnect(client, userdata, flags, rc=0):
    log.write("disconnection success. "+str(flags)+ "result code : " + str(rc))
    if log != None :
        log.close()


def on_subscribe(client,userdata,mid,granted_qos):
    log.write("subscribed : " + TOPIC + " qos : "+ str(granted_qos))

def on_message(client,userdata,msg):
    
    # 실제로는 json data로 받고 sensor와 car_number를 더 쉽게 파싱할 수 있음.
    # 지금은 0 번째 숫자로 추가인지 아닌지 가리고, 1,2번째 숫자가 sensor값(혹은 차 넘버),
    #3번째 숫자가 machine 고유 번호임.
    
    data=str(msg.payload.decode("utf-8"))
    is_add=data[0]
    sensor_or_car_number=data[1:3]
    machine_id=data[3:]
    token='Token ' + Token
    
    headers={'Authorization' : token}
    
    if is_add=='1':
        log.write("is_add : " + is_add + " car_number : " + sensor_or_car_number + " machine_id : " + machine_id)
        data={ "id" : int(machine_id), "car_number" : sensor_or_car_number }
        res=requests.get(URL+'api/machine/',headers=headers,data=data)
        if res.status_code ==201:
            log.write( str(res.status_code) + " successfully add machine " + machine_id + " " + str(res.json()["pub_date"]))
        else :
            log.write( str(res.status_code) + " error add machine. " + machine_id)
            log.write( res.text )
        #postgres_machine_add(DB_HOST,DB_USER,DB_PASSWORD,DB,sensor_or_car_number,machine_id)
    else :
        log.write("is_add : " + is_add + " sensor : " + sensor_or_car_number + " machine_id : " + machine_id)
        data={ "machine" : int(machine_id), "sensor" : int(sensor_or_car_number) }
        res=requests.get(URL+'api/sensor/',headers=headers,data=data)
        if res.status_code == 201:
            log.write( str(res.status_code) + "successfully updating sensor data. " + machine_id + " " + str(res.json()["pub_date"]))
        else :
            log.write( str(res.status_code) + "error updating sensor data. " + machine_id)
            log.write( res.text )
        
        #postgres_sensor_insert(DB_HOST,DB_USER,DB_PASSWORD,DB,sensor_or_car_number,machine_id)

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

if log != None :
    log.close()
