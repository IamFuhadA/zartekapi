from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Ride
from .serializers import UserSerializer, RideSerializer

# Create your views here.
@csrf_exempt
def userApi(request, id=0):
    if request.method == "POST":
        user_data = JSONParser().parse(request)
        if 'register' in request.path:
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                token, _ = Token.objects.get_or_create(user=user)
                return JsonResponse({"token": token.key, "user": user_serializer.data}, safe=False)
            return JsonResponse(user_serializer.errors, safe=False, status=400)
    return JsonResponse("Not allowed", safe=False, status=405)

@csrf_exempt
def rideApi(request, id=0):
    if request.method == "GET":
        if id != 0:
            try:
                ride = Ride.objects.get(id=id)
                ride_serializer = RideSerializer(ride)
                return JsonResponse(ride_serializer.data, safe=False)
            except Ride.DoesNotExist:
                return JsonResponse("Ride not found", safe=False, status=404)
        else:
            rides = Ride.objects.all()
            ride_serializer = RideSerializer(rides, many=True)
            return JsonResponse(ride_serializer.data, safe=False)
            
    elif request.method == "POST":
        ride_data = JSONParser().parse(request)
        ride_serializer = RideSerializer(data=ride_data)
        if ride_serializer.is_valid():
            rider_id = ride_data.get('rider')
            if rider_id:
                rider = User.objects.get(id=rider_id)
                ride_serializer.save(rider=rider)
            else:
                ride_serializer.save() 
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False, status=400)

@csrf_exempt
def rideUpdateApi(request, id):
    # Specialized for status updates and location
    if request.method == "POST" or request.method == "PUT":
        data = JSONParser().parse(request)
        try:
            ride = Ride.objects.get(id=id)
            if 'status' in data:
                ride.status = data['status']
            if 'latitude' in data:
                ride.current_latitude = data['latitude']
            if 'longitude' in data:
                ride.current_longitude = data['longitude']
            if 'driver' in data:
                ride.driver = User.objects.get(id=data['driver'])
                ride.status = 'ACCEPTED'
            ride.save()
            return JsonResponse("Updated Successfully", safe=False)
        except (Ride.DoesNotExist, User.DoesNotExist):
            return JsonResponse("Failed to Update", safe=False, status=400)
    return JsonResponse("Method not allowed", safe=False, status=405)

@csrf_exempt
def rideMatchingApi(request):
    if request.method == "GET":
        rides = Ride.objects.filter(status='REQUESTED')
        ride_serializer = RideSerializer(rides, many=True)
        return JsonResponse(ride_serializer.data, safe=False)
    return JsonResponse("Method not allowed", safe=False, status=405)
