from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
import os
import json
from .models import *
from .serializers import *
from .permissions import *
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
import requests
import hashlib
import datetime

Crawler_URL='http://crawler.auton-iot.com/api/gps/'
# Create your views here.

class MyUserViewset(ModelViewSet):
    queryset=MyUser.objects.all()
    serializer_class=MyUserSerializer
    permission_classes=[IsAuthenticated,]
    authentication_classes=[TokenAuthentication]
    def list(self, request):
        if request.user.is_staff :
            return super().list
        else :
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
def hash_machineid(raw_id):
    data=(raw_id).encode()
    hash_object=hashlib.sha256()
    hash_object.update(data)
    hex_dig=hash_object.hexdigest()
    return (hex_dig)
    

    
class MachineViewset(ModelViewSet):
    queryset=Machine.objects.all()
    serializer_class=MachineSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[TokenAuthentication]
    @action(detail=False,methods=['post'])
    def qr_create(self, request):
        data = JSONParser().parse(request)
        serializer = MachineSerializer(data=data)
        if serializer.is_valid():
            
            id=serializer.data['id']
            
            machine_id=hash_machineid(raw_id=id)
        # raw id를 hash화 시킴.
            try :
                m=Machine.objects.create(id=machine_id)
            except :
                return HttpResponse('Maybe there is already same machine, or other error occurs.',status=423)
        # Machine의 id를 hash id로 업데이트.
        # 해당 머신을 가지고...
        # qr코드를 생성해냄.
        # 근데 얘가 response가 될 수는 없겠지.
            m.qr_set.create(qr='https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=' + (machine_id))
            return JsonResponse({ 'id' : m.id},status=201)
        return HttpResponse(status=500)
    
class QRViewset(ReadOnlyModelViewSet):
    queryset=QR.objects.all()
    serializer_class=QRSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[TokenAuthentication]
    #authentication_classes=[SessionAuthentication,BasicAuthentication]
    
    
def find_point(gps_string):

    point=[]
    gps_string=gps_string.split(';')[1]
    gps_string=gps_string.replace('(',"")
    gps_string=gps_string.replace(')',"")
    point.append(gps_string.split(' ')[1])
    point.append(gps_string.split(' ')[2])
    return point

class GPSViewset(ModelViewSet):
    queryset=GPS.objects.all()
    serializer_class=GPSSerializer
    permission_classes=[IsAuthenticated,]#OnlyRightUserUpdateAvailable]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}
    @action(detail=False,methods=['post'])
    def find_airkorea(self, request):
        data = JSONParser().parse(request)
            
        serializer = GPSSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            d=serializer.data['gps']
            
            point=find_point(d)
            shell='curl "http://crawler.auton-iot.com/api/gps/?X='+point[0]+'&Y='+point[1]+'"'
            stream=os.popen(shell)
            #res=requests.post(Crawler_URL,data={'gps' : d},timeout=timeout)
        # 여기서 DMZ의 AirKorea API Crawler에게 데이터를 요청하고 (request library), 돌려받은 데이터를 이용하여 AirKorea를 add 한다.

            #if res.status_code !=201 :
            #    return HttpResponse(status = res.status_code)
            output=stream.read()
            ar=json.loads(output)
            m=Machine.objects.get(id=serializer.data['machine'])
            m.airkorea_set.create(airkorea=ar["airkorea"])
        
        return JsonResponse(serializer.data,status=201)

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
