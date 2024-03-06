from django.shortcuts import render
from .views import CustomLoginView
from django.urls import path

app_name = "users"

urlpatterns = [
  path('login/', CustomLoginView.as_view(), name='login'),
   ]