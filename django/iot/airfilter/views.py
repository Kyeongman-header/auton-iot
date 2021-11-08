from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
import datetime
# Create your views here.

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
        serializer = Seven_Days_Serializer(query_set,many=True)
        return JsonResponse(serializer.data, safe=False)

def latest_thirty_days(request,id):

    query_set = Machine.objects.get(id=id).thirty_days_set.all()

    if request.method == 'GET':
        serializer = Thirty_Days_Serializer(query_set,many=True)
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
