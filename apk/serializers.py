from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class RideSerializer(serializers.ModelSerializer):
    rider_name = serializers.ReadOnlyField(source='rider.username')
    driver_name = serializers.ReadOnlyField(source='driver.username')

    class Meta:
        model = Ride
        fields = [
            'id', 'rider', 'rider_name', 'driver', 'driver_name',
            'pickup_location', 'dropoff_location', 'status',
            'current_latitude', 'current_longitude',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['rider', 'status', 'created_at', 'updated_at']
