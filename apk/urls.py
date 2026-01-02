from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^user/register/$', views.userApi),
    re_path(r'^ride/$', views.rideApi),
    re_path(r'^ride/([0-9]+)$', views.rideApi),
]
