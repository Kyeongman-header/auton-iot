import paho.mqtt.client as mqtt
import psycopg2 as pg2
import datetime
import json

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
        print("-----------------\n postgre sql connection error :( \n ---------------------")
        print(e)
        return
    cur=conn.cursor()
    query=f"INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES ({machine_id} {car_number},current_timestamp)"
    try :
        cur.execute("INSERT INTO airfilter_machine(id,car_number,pub_date) VALUES (%s, %s,current_timestamp)",(machine_id,car_number))
        conn.commit()
    except pg2.DatabaseError as dberror:
        print("-----------------------\m insert query to machine table error :(\n ----------------------")
        print(dberror)
        conn.rollback()
    else :
        print("insert success")
        print(query)
    conn.close()

def postgres_sensor_insert(host,user,password,db,sensor,machine_id):
    try:
        conn=pg2.connect(host=host,dbname=db,user=user,password=password)
    except Exception as e:
        print("-----------------\npostgre sql connection error :(\n--------------------")
        print(e)
        return

    cur=conn.cursor()
    n=datetime.datetime.now()
    query=f"INSERT INTO airfilter_sensor VALUES ('{sensor}','{n}','{machine_id}')"
    
    try :
        cur.execute("INSERT INTO airfilter_sensor (machine_id,sensor,pub_date)VALUES (%s, %s, current_timestamp)",(machine_id,sensor))
        conn.commit()
    except pg2.DatabaseError as dberror:
        print("------------------------\ninsert query to sensor table error :(\n-----------------------")
        print(dberror)
        conn.rollback()
    else :
        print("insert success : ")
        print(query)

    conn.close()


def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("Broker connected")
    else:
        print("Broker connection failure : " + str(rc))

def on_disconnect(client, userdata, flags, rc=0):
    print("disconnection success. "+str(flags)+ "result code : " + str(rc))


def on_subscribe(client,userdata,mid,granted_qos):
    print("subscribed : " + TOPIC + " qos : "+ str(granted_qos))

def on_message(client,userdata,msg):
    
    # 실제로는 json data로 받고 sensor와 car_number를 더 쉽게 파싱할 수 있음.
    # 지금은 0 번째 숫자로 추가인지 아닌지 가리고, 1,2번째 숫자가 sensor값(혹은 차 넘버),
    #3번째 숫자가 machine 고유 번호임.
    
    data=str(msg.payload.decode("utf-8"))
    is_add=data[0]
    sensor_or_car_number=data[1:3]
    machine_id=data[3:]

    if is_add=='1':
        print("is_add : " + is_add + " car_number : " + sensor_or_car_number + " machine_id : " + machine_id)
        postgres_machine_add(DB_HOST,DB_USER,DB_PASSWORD,DB,sensor_or_car_number,machine_id)
    else :
        print("is_add : " + is_add + " sensor : " + sensor_or_car_number + " machine_id : " + machine_id)
        postgres_sensor_insert(DB_HOST,DB_USER,DB_PASSWORD,DB,sensor_or_car_number,machine_id)

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

print("rc: " + str(rc))
