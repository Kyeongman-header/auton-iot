from django.urls import path
from . import views

urlpatterns=[
    path('machines_list/',views.machines_list),
    path('machine/<int:pk>/',views.address),
    path('login/',views.login),
    url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework'))
    ]
