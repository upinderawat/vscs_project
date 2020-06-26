from django.contrib import admin
from django.urls import path
from . import views

app_name='merchant'

urlpatterns = [
    path('', views.index),
]
