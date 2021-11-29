#!/bin/bash





if [ -e /usr/lib/systemd/system/nginx.service ] 
then
sudo service nginx restart
sudo /usr/bin/python3 /home/ubuntu/django/iot/manage.py collectstatic
fi

if [ -e /etc/systemd/system/gunicorn.service ] 
then
sudo service gunicorn restart
fi

if [ -d /usr/local/lib/python3.8/dist-packages/django_crontab ]
then
#sudo /usr/bin/python3 /home/ubuntu/django/iot/manage.py crontab remove
sudo /usr/bin/python3 /home/ubuntu/django/iot/manage.py crontab add
fi
