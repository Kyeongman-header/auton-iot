#!/bin/bash

if [ ! -d /usr/local/lib/python3.8/dist-packages/gunicorn ]
then
        printf "gunicorn was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
        pip install gunicorn
        printf "[Unit]\nDescription=gunicorn daemon\nAfter=network.target\n\n[Service]\nUser=ubuntu\nGroup=ubuntu\nWorkingDirectory=/home/ubuntu/django/iot\nExecStart=/usr/local/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 iot.wsgi:application\n[Install]\nWantedBy=multi-user.target\n" > /etc/systemd/system/gunicorn.service
        systemctl daemon-reload
        systemctl start gunicorn
        systemctl enable gunicorn

fi

if [ ! -d /usr/local/lib/python3.8/dist-packages/psycopg2 ]
then
        printf "psycopg2(python postgresql) was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
        pip install psycopg2-binary
fi


if [ ! -d /usr/local/lib/python3.8/dist-packages/django ]
then
        printf "django was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
        pip install django
fi

if [ ! -d /usr/local/lib/python3.8/dist-packages/rest_framework ]
then
        printf "django rest framework was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
        pip install djangorestframework
fi


if [ ! -d /usr/local/lib/python3.8/dist-packages/django_crontab ]
then
        printf "django_crontab was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
        pip install django-crontab
fi

if [ ! -d /usr/local/lib/python3.8/dist-packages/django_filters ]
then
	printf "django_filter was not installed in pip. installing that library.\n" >> /tmp/code_deploy_script_checker.log
	pip install django-filter
fi

if [ ! -d /usr/local/lib/python3.8/dist-packages/django_rest_auth ]
then
	printf "django-rest-auth was not installed in pip. installing that library.\n" >> /tmp/code_deploy_scripts_checker.log
	pip install django-rest-auth django-allauth
fi
