from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
import datetime

# Create your views here.

class MyUserViewset(ModelViewSet):
    queryset=MyUser.objects.all()
    serializer_class=MyUserSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[SessionAuthentication,BasicAuthentication]


class MachineViewset(ModelViewSet):
    queryset=Machine.objects.all()
    serializer_class=MachineSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]


class SensorViewset(ModelViewSet):
    queryset=Sensor.objects.all()
    serializer_class=SensorSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication] 
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}

class AirKoreaViewset(ModelViewSet):
    queryset=AirKorea.objects.all()
    serializer_class=AirKoreaSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}

class SevenDaysViewset(ReadOnlyModelViewSet):
    queryset=Seven_Days.objects.all()
    serializer_class=SevenDaysSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}

class ThirtyDaysViewset(ReadOnlyModelViewSet):
    queryset=Thirty_Days.objects.all()
    serializer_class=ThirtyDaysSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}


# @csrf_exempt
# def machines_list(request):
#     if request.method == 'GET':
#         query_set = Machine.objects.all()
#         serializer = MachineSerializer(query_set, many=True)
#         return JsonResponse(serializer.data, safe=False)
# @csrf_exempt
# def machine(request, id):

#     obj = Machine.objects.get(id=id)

#     if request.method == 'GET':
#         serializer = MachineSerializer(obj)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = MachineSerializer(obj, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         obj.delete()
#         return HttpResponse(status=204)
#def new_LoginView(request):
#    if request.method == "GET":
#        return render(reqeust,"airfilter/login.html")
#    elif request.method == "POST":
#        user_id= request.POST.get('user_id')
#        user_pw= request.POST.get('user_pw')
#        user=authenticate(request,username=user_id,password=user_pw)
#        if user is not None :
#            login(request,user=user)
#            return redirect('')
