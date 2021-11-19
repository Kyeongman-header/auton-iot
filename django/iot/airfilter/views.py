from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action

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
    permission_classes=[IsAdminUser,]
    authentication_classes=[SessionAuthentication,BasicAuthentication]

    
def hash_machinid(raw_id):
    data=b(str(id)).encode()
    hash_object=hashlib.sha256()
    hash_object.update(data)
    hex_dig=hash_object.hexdigest()
    return int(hex_dig,16)
    

class MachineViewset(ModelViewSet):
    queryset=Machine.objects.all()
    serializer_class=MachineSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    @action(detail=False,methods=['post'])
    def qr_create(self, request):
        data = JSONParser().parse(request)
        serializer = view.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            id=serializer.data['id']
        
            machine_id=hash_machineid(raw_id=id)
        # raw id를 hash화 시킴.
        
            Machine.objects.get(id=id).update(id=machine_id)
        # Machine의 id를 hash id로 업데이트.
        
            m=Machine.objects.get(id=machine_id)
        # 해당 머신을 가지고...
        # qr코드를 생성해냄.
        # 근데 얘가 response가 될 수는 없겠지.
            m.qr_set.create(qr='https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=' + str(machine_id))
            return JsonResponse(serializer.data,status-201)
        return HttpResponse(status=500)
    
class QRViewset(ReadOnlyModelViewSet):
    queryset=QR.objects.all()
    serializer_class=QRSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[SessionAuthentication,BasicAuthentication]
    
    
    
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
            res=requests.post(Crawler_URL,data={'gps' : d})
        # 여기서 DMZ의 AirKorea API Crawler에게 데이터를 요청하고 (request library), 돌려받은 데이터를 이용하여 AirKorea를 add 한다.
        # Crawler_URL='http://crawler.auton-iot.com/api/gps/'
            if res.status_code !=200 :
                return HttpResponse(status_code = res.status_code)
            
            m=Machine.objects.get(id=serializer.data['machine'])
            m.airkorea_set.create(airkorea=res.json())
        
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
