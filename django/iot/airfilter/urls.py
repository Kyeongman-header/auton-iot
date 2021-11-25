from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import url,include

router=DefaultRouter()
router.register('user',views.MyUserViewset)
router.register('machine',views.MachineViewset)
router.register('gps',views.GPSViewset)
router.register('qr',views.QRViewset)
router.register('sensor',views.SensorViewset)
router.register('airkorea',views.AirKoreaViewset)
router.register('seven_days',views.SevenDaysViewset)
router.register('thirty_days',views.ThirtyDaysViewset)



urlpatterns=[
    path('mqtt_postgres/',views.OnlyMQTTSensorAdd.as_view())
    path('api/',include(router.urls)),
    #url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
    ]
