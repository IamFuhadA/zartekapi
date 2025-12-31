from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Ride
import json

class RideSharingTests(APITestCase):
    def setUp(self):
        self.rider_user = User.objects.create_user(username='rider', password='password123')
        self.driver_user = User.objects.create_user(username='driver', password='password123')
        
    def test_user_registration(self):
        url = '/api/user/register/'
        data = {'username': 'newuser', 'password': 'newpassword123', 'email': 'new@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # In user's level, they often return 200 for success
        self.assertIn('token', response.json())

    def test_create_ride(self):
        url = '/api/ride/'
        data = {
            'pickup_location': '123 Main St',
            'dropoff_location': '456 Elm St',
            'rider': self.rider_user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "Added Successfully")

    def test_get_rides(self):
        Ride.objects.create(rider=self.rider_user, pickup_location='A', dropoff_location='B')
        url = '/api/ride/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_accept_ride(self):
        ride = Ride.objects.create(rider=self.rider_user, pickup_location='A', dropoff_location='B')
        url = f'/api/ride/update/{ride.id}'
        data = {'driver': self.driver_user.id}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), "Updated Successfully")
        
        ride.refresh_from_db()
        self.assertEqual(ride.status, 'ACCEPTED')
        self.assertEqual(ride.driver, self.driver_user)

    def test_status_update(self):
        ride = Ride.objects.create(rider=self.rider_user, driver=self.driver_user, status='ACCEPTED', pickup_location='A', dropoff_location='B')
        url = f'/api/ride/update/{ride.id}'
        
        # Start ride
        response = self.client.post(url, {'status': 'STARTED'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ride.refresh_from_db()
        self.assertEqual(ride.status, 'STARTED')

    def test_ride_matching(self):
        Ride.objects.create(rider=self.rider_user, status='REQUESTED', pickup_location='A', dropoff_location='B')
        url = '/api/ride/matching/'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_track_simulation(self):
        ride = Ride.objects.create(rider=self.rider_user, pickup_location='A', dropoff_location='B')
        url = f'/api/ride/update/{ride.id}'
        
        response = self.client.post(url, {'latitude': 10.0, 'longitude': 20.0}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        ride.refresh_from_db()
        self.assertEqual(ride.current_latitude, 10.0)
