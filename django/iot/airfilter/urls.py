from django.urls import path
from . import views
from django.conf.urls import url,include

urlpatterns=[
    path('',views.index,name='index'),
    path('machines_list/',views.machines_list),
    path('machine/<int:id>/',views.machine),
    path('latest_sensor/<int:id>/',views.latest_sensor),
    path('latest_airkorea/<int:id>/',views.latest_airkorea),
    path('today_sensor/<int:id>/',views.hours_sensor),
    path('today_airkorea/<int:id>/',views.hours_airkorea),
    path('seven_days/<int:id>/',views.latest_seven_days),
    path('thirty_days/<int:id>/',views.latest_thirty_days),
    #path('login/',views.login),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
    ]
