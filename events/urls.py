"""events URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from app import views

urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),

    path('events/<str:date>', views.events, name='events'),
    path('event/<int:eid>/', views.patient, name='event'),
    path('event/create/', views.event, name='create_event'),
    path('event/create/<str:date>', views.event_on_date, name='create_event_on_date'),
    path('event/<int:eid>/', views.event, name='edit_event'),
    
    path('patients/', views.patients, name='patients'),
    path('patient/<int:pid>/', views.patient, name='patient'),
    path('patient/create/', views.edit_patient, name='create_patient'),
    path('patient/edit/<int:pid>/', views.edit_patient, name='edit_patient'),
]
