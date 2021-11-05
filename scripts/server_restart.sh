#!/bin/bash

if [ -e /etc/systemd/system/gunicorn.service ] then
  sudo service gunicorn restart
  
if [ -e /usr/lib/systemd/system/nginx.service ] then
  sudo service nginx restart

if [ -e /usr/lib/systemd/system/mosquitto.service ] then
  sudo service mosquitto restart

if [ -e /usr/lib/systemd/system/mqtt_postgres.service ] then
  sudo service mqtt_postgres restart
