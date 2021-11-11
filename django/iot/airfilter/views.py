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


#def index(request):
#    url_list=["machines_list/","machine/기계 아이디","latest_sensor/기계 아이디","latest_airkorea/기계 아이디","today_sensor/기계 아이디","today_airkorea/기계 아이디", "seven_days/기계 아이디", "thirty_days/기계 아이디"]
#    context={'url_list':url_list}
#    return render(request,'airfilter/index.html',context)

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
    #def get_permissions(self):
    #    if self.action=='list' or self.action=='retrieve' :
    #        permission_classes=[IsAuthenticated]
    #    else :
    #        permission_classes=[IsAdminUser]


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
    

@csrf_exempt
def machines_list(request):
    if request.method == 'GET':
        query_set = Machine.objects.all()
        serializer = MachineSerializer(query_set, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def machine(request, id):

    obj = Machine.objects.get(id=id)

    if request.method == 'GET':
        serializer = MachineSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = MachineSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)

@csrf_exempt
def latest_sensor(request,id):

    obj = Machine.objects.get(id=id).sensor_set.latest('pub_date')

    if request.method == 'GET':
        serializer = SensorSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SensorSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)

@csrf_exempt
def hours_sensor(request,id):
    query_set=Machine.objects.get(id=id).sensor_set.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days=1))
    if request.method == 'GET':
        serializer=SensorSerializer(query_set,many=True)
        return JsonResponse(serializer.data,safe=False)

@csrf_exempt
def hours_airkorea(request,id):
    query_set=Machine.objects.get(id=id).airkorea_set.filter(pub_date__gte=datetime.datetime.now()-datetime.timedelta(days=1))
    if request.method=='GET':
        serializer=AirKoreaSerializer(query_set,many=True)
        return JsonResponse(serializer.data,safe=False)

@csrf_exempt
def latest_airkorea(request,id):

    obj = Machine.objects.get(id=id).airkorea_set.latest('pub_date')

    if request.method == 'GET':
        serializer = AirKoreaSerializer(obj)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = AirKoreaSerializer(obj, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return HttpResponse(status=204)

@csrf_exempt
def latest_seven_days(request,id):

    query_set = Machine.objects.get(id=id).seven_days_set.all()

    if request.method == 'GET':
        serializer = SevenDaysSerializer(query_set,many=True)
        return JsonResponse(serializer.data, safe=False)

def latest_thirty_days(request,id):

    query_set = Machine.objects.get(id=id).thirty_days_set.all()

    if request.method == 'GET':
        serializer = ThirtyDaysSerializer(query_set,many=True)
        return JsonResponse(serializer.data, safe=False)

# AUTH 관련한 것은 TOKEN으로 하기로 했지. 조금 나중에 생각하자.
#@csrf_exempt
#def login(request):
#    if request.method == 'POST':
#
#        print("request "+ str(request))
#        print("body "+ str(request.body))
#        userid = request.POST.get("userid", "")
#        userpw = request.POST.get("userpw", "")
#        login_result = authenticate(username=userid, password=userpw)
#
#        print("userid = " + userid + " result = " + str(login_result))
#        if login_result:
#            return HttpResponse(status=200)
#        else:
#            return render(request, "addresses/login.html", status=401)
#
#
#    return render(request, "addresses/login.html")
