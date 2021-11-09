#!/bin/bash

if [ -e /etc/systemd/system/gunicorn.service ] 
then
sudo service gunicorn restart
fi

if [ -e /usr/lib/systemd/system/nginx.service ] 
then
sudo service nginx restart
fi

if [ -e /usr/lib/systemd/system/mosquitto.service ]
then
sudo service mosquitto restart
fi

if [ -e /usr/lib/systemd/system/mqtt_postgres.service ]
then
sudo service mqtt_postgres restart
fi

if [ ! -d /usr/local/lib/python3.8/dist-packages/django_crontab ]
then
sudo /usr/bin/python3 /home/ubuntu/django/iot/manage.py crontab add
fi
