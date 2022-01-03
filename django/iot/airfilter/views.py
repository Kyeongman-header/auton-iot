from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser, AllowAny
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
from rest_framework.generics import CreateAPIView
from django_filters.rest_framework import DjangoFilterBackend, filters
import django_filters
from django.core import serializers
import requests
import hashlib
import datetime

Crawler_URL='http://crawler.auton-iot.com/api/gps/'
# Create your views here.


class OnlyMQTTSensorAdd(CreateAPIView,):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[TokenAuthentication]
    def create(self, request): # 임시로, sensor가 전송될때 P.M 2.5 _ 2 값을 AIR KOREA 값으로 전송한다.(가장 정확한 외부 공기질) (그러나 상용화 단계에선 어차피 못씀. 걍 지워버리면 되는 코드임.)
        data = JSONParser().parse(request)
        serializer_sensor=SensorSerializer(data=data)

        if serializer_sensor.is_valid() :
            serializer_sensor.save()
            m=Machine.objects.get(id=serializer_sensor.data['machine'])
            m.airkorea_set.create(airkorea={'P.M 2.5' : data['sensor']['P.M 2.5_2'], 'CO' : 0,'SO2' : 0,'O3' : 0,'NO2' : 0,'khai' : 0})
            if m.hours_sensor_set.exists() :
                if m.hours_sensor_set.last().pub_date.hour == datetime.datetime.now().hour:
                    number=m.hours_sensor_set.last().number
                    m.hours_sensor_set.last().update(hours=((m.hours_sensor_set.last().hours*number) + data['sensor']['P.M 2.5']) / (number+1) , number=number+1)
                else :
                    m.hours_sensor_set.create(hours=data['sensor']['P.M 2.5'], number=1)
                
           
            if m.days_sensor_set.exists() :    
                if m.days_sensor_set.last().pub_date.day == datetime.datetime.now().day:
                    number=m.days_sensor_set.last().number
                    m.days_sensor_set.last().update(days=((m.days_sensor_set.last().days*number) + data['sensor']['P.M 2.5']) / (number+1) , number=number+1)
                else :
                    m.days_sensor_set.create(days=data['sensor']['P.M 2.5'], number=1)
            
                
            if m.weeks_sensor_set.exists() :    
                if  (datetime.datetime.now() - m.weeks_sensor_set.last().pub_date).days/7 < 1:
                    number=m.weeks_sensor_set.last().number
                    m.weeks_sensor_set.last().update(weeks=((m.weeks_sensor_set.last().weeks*number) + data['sensor']['P.M 2.5']) / (number+1) , number=number+1)
                else :
                    m.weeks_sensor_set.create(weeks=data['sensor']['P.M 2.5'], number=1)                
        return JsonResponse(serializer_sensor.data,status=201)

class MyUserViewset(ReadOnlyModelViewSet):
    queryset=MyUser.objects.all()
    serializer_class=MyUserSerializer
    permission_classes=[IsAdminUser]
    authentication_classes=[TokenAuthentication]

    
def hash_machineid(raw_id):
    data=(raw_id).encode()
    hash_object=hashlib.sha256()
    hash_object.update(data)
    hex_dig=hash_object.hexdigest()
    return (hex_dig)
    
class MachineViewset(ModelViewSet):
    queryset=Machine.objects.all()
    serializer_class=MachineSerializer
    permission_classes=[IsAuthenticated,]
    authentication_classes=[TokenAuthentication]
    
    def partial_update(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    def create(self, request):
        # 생성 작업은 admin과 factory만 가능하다.
        if not request.user.is_staff :
            return HttpResponse(status=405) 
        data = JSONParser().parse(request)
        serializer = MachineSerializer(data=data)
        if serializer.is_valid():
            
            id=serializer.data['id']
            machine_id=id
            # for only 고등기술연구원 test. 
            # 이후 다시 밑의 코드를 사용할것!!!!!
        #    machine_id=hash_machineid(raw_id=id)
        # raw id를 hash화 시킴.
            try :
                m=Machine.objects.create(id=machine_id)
            except :
                return HttpResponse('Maybe there is already same machine, or other error occurs.',status=423)
        # Machine의 id를 hash id로 업데이트.
        # 해당 머신을 가지고...
        # qr코드를 생성해냄.
        # 근데 얘가 response가 될 수는 없겠지.
            m.qr_set.create(qr='https://chart.googleapis.com/chart?cht=qr&chs=200x200&chl=' + (machine_id), raw_id=id)
            return JsonResponse({ 'id' : m.id},status=201)
        return HttpResponse(status=500)
    
    def list(self, request):
        if request.user.is_staff :
            return super().list(request)
        else :
            return HttpResponse(status=405)        
    def destroy(self, request, pk=None):
        if request.user.is_staff :
            return super().destroy(request,pk)
        else :
            return HttpResponse(status=405)

    
    
    
class QRViewset(ReadOnlyModelViewSet):
    queryset=QR.objects.all()
    serializer_class=QRSerializer
    permission_classes=[IsAdminUser,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}

    
    
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
    
    def create(self, request):
        data = JSONParser().parse(request)
        try :
            m=request.user.machine
        except :
            return HttpResponse("No machine registered in that user.", status=405)
        
        data['machine']=m.id
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
    
    def list(self, request):
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            
            gpss=m.gps_set.all() # gps 데이터는 상용 단계에서 저장되지 않는다. 
            gps_jsons=GPSSerializer(gpss,many=True).data
            return JsonResponse(gps_jsons,status=200,safe=False)
        
    def destroy(self, request, pk=None):
        if request.user.is_staff :
            return super().destroy(request,pk)
        else :
            return HttpResponse(status=405)    
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)

class SensorViewset(ReadOnlyModelViewSet):
    queryset=Sensor.objects.all()
    serializer_class=SensorSerializer
    permission_classes=[AllowAny] # for 통신 테스트 with 고등기술연구원.
    #permission_classes=[AdminWriteOrUserReadOnly,]
    #authentication_classes=[TokenAuthentication] 
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}
    def list(self,request):
        user=request.user

            
# test를 위해서 잠시 보안 관련된 것은 접어놓는다.
    def list(self, request):
        user=request.user
        user.last_login=timezone.localtime()
        user.save(update_fields=['last_login'])
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            sensors=m.sensor_set.last() # 실시간에서만 쓸 거니깐 가장 마지막 데이터만.
            sensor_jsons=SensorSerializer(sensors,many=True).data
            return JsonResponse(sensor_jsons,status=200,safe=False)
        
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)
        
        #날짜를 pick하기 위한 사용자 정의 필터.
class TimeRangeFilter_Hours(django_filters.FilterSet):
    pub_date_gte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='gte')
    pub_date_lte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='lte')
    class Meta:
        model = Hours_sensor
        fields = ['machine','pub_date_gte','pub_date_lte']
        
class HoursViewset(ReadOnlyModelViewSet):
    queryset=Hours_sensor.objects.all()
    serializer_class=HoursSensorSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_class=TimeRangeFilter_Hours
    def list(self, request):
        user=request.user
        user.last_login=timezone.localtime()
        user.save(update_fields=['last_login'])
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            hours=m.hours_sensor_set.filter(pub_date__gte=(datetime.datetime.now()-datetime.timedelta(days=1))).all()
            
            hours_jsons=HoursSensorSerializer(hours,many=True).data
            return JsonResponse(hours_jsons,status=200,safe=False)
        
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)           

        
class TimeRangeFilter_Days(django_filters.FilterSet):
    pub_date_gte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='gte')
    pub_date_lte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='lte')
    class Meta:
        model = Days_sensor
        fields = ['machine','pub_date_gte','pub_date_lte']
                
class DaysViewset(ReadOnlyModelViewSet):
    queryset=Days_sensor.objects.all()
    serializer_class=DaysSensorSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_class=TimeRangeFilter_Days
    def list(self, request):
        user=request.user
        user.last_login=timezone.localtime()
        user.save(update_fields=['last_login'])
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            days=m.days_sensor_set.filter(pub_date__gte=(datetime.datetime.now()-datetime.timedelta(days=7))).all()
            
            days_jsons=DaysSensorSerializer(days,many=True).data
            return JsonResponse(days_jsons,status=200,safe=False)
        
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)        
        
class TimeRangeFilter_Weeks(django_filters.FilterSet):
    pub_date_gte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='gte')
    pub_date_lte = django_filters.DateTimeFilter(field_name="pub_date", lookup_expr='lte')
    class Meta:
        model = Weeks_sensor
        fields = ['machine','pub_date_gte','pub_date_lte']
        
class WeeksViewset(ReadOnlyModelViewSet):
    queryset=Weeks_sensor.objects.all()
    serializer_class=WeeksSensorSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_class=TimeRangeFilter_Weeks
    def list(self, request):
        user=request.user
        user.last_login=timezone.localtime()
        user.save(update_fields=['last_login'])
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            weeks=m.weeks_sensor_set.filter(pub_date__gte=(datetime.datetime.now()-datetime.timedelta(weeks=7))).all()
            
            weeks_jsons=WeeksSensorSerializer(weeks,many=True).data
            return JsonResponse(weeks_jsons,status=200,safe=False)
        
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)           
        
class AirKoreaViewset(ReadOnlyModelViewSet):
    queryset=AirKorea.objects.all()
    serializer_class=AirKoreaSerializer
    permission_classes=[AdminWriteOrUserReadOnly,]
    authentication_classes=[TokenAuthentication]
    filter_backends=(DjangoFilterBackend,)
    filter_fields={'machine'}
    def list(self, request):
        user=request.user
        user.last_login=timezone.localtime()
        user.save(update_fields=['last_login'])
        if request.user.is_staff :
            return super().list(request)
        else :
            try :
                m=request.user.machine
            except :
                return HttpResponse("No machine registered in that user.", status=405)
            airkoreas=m.airkorea_set.last()
            
            airkorea_jsons=AirKoreaSerializer(airkoreas,many=True).data
            return JsonResponse(airkorea_jsons,status=200,safe=False)
        
    def retrieve(self, request,pk=None):
        if request.user.is_staff :
            return super().retrieve(request,pk)
        else :
            return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)   
        
# class SevenDaysViewset(ReadOnlyModelViewSet):
#     queryset=Seven_Days.objects.all()
#     serializer_class=SevenDaysSerializer
#     permission_classes=[AdminWriteOrUserReadOnly,]
#     authentication_classes=[TokenAuthentication]
#     filter_backends=(DjangoFilterBackend,)
#     filter_fields={'machine'}
#     def list(self, request):
#         user=request.user
#         user.last_login=timezone.localtime()
#         user.save(update_fields=['last_login'])
#         if request.user.is_staff :
#             return super().list(request)
#         else :
#             try :
#                 m=request.user.machine
#             except :
#                 return HttpResponse("No machine registered in that user.", status=405)
#             sevendayss=m.seven_days_set.filter(pub_date__gte=(datetime.datetime.now()-datetime.timedelta(days=31))).all() # 한달치 데이터.
#             sevendays_jsons=SevenDaysSerializer(sevendayss,many=True).data
#             return JsonResponse(sevendays_jsons,status=200,safe=False)
#     def retrieve(self, request,pk=None):
#         if request.user.is_staff :
#             return super().retrieve(request,pk)
#         else :
#             return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)   
        
# class ThirtyDaysViewset(ReadOnlyModelViewSet):
#     queryset=Thirty_Days.objects.all()
#     serializer_class=ThirtyDaysSerializer
#     permission_classes=[AdminWriteOrUserReadOnly,]
#     authentication_classes=[TokenAuthentication]
#     filter_backends=(DjangoFilterBackend,)
#     filter_fields={'machine'}
#     def list(self, request):
#         user=request.user
#         user.last_login=timezone.localtime()
#         user.save(update_fields=['last_login'])
#         if request.user.is_staff :
#             return super().list(request)
#         else :
#             try :
#                 m=request.user.machine
#             except :
#                 return HttpResponse("No machine registered in that user.", status=405)
#             thirtydayss=m.thirty_days_set.filter(pub_date__gte=(datetime.datetime.now()-datetime.timedelta(days=31))).all() # 한달치 데이터.
#             thirtydays_jsons=ThirtyDaysSerializer(thirtydayss,many=True).data
#             return JsonResponse(thirtydays_jsons,status=200,safe=False)
#     def retrieve(self, request,pk=None):
#         if request.user.is_staff :
#             return super().retrieve(request,pk)
#         else :
#             return HttpResponse("You may not access directly database. You can access data with your machine id",status=405)   

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
