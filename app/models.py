from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from app.managers import PatientManager, EventManager, ProcedureManager, ProfileManager

class Patient(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    objects = PatientManager()

    def __str__(self):
        return '{}'.format(self.name)

class Procedure(models.Model):
    title = models.CharField(max_length=200)
    ref_num = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    objects = ProcedureManager()

    def __str__(self):
        return '{}'.format(self.title)

class Event(models.Model):
    date = models.DateField()
    price = models.PositiveIntegerField(default=0)
    medication = models.CharField(max_length=400, blank=True)
    body_area = models.CharField(max_length=400, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    procedures = models.ManyToManyField(Procedure, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    objects = EventManager()

    @property
    def get_html_url(self):
        url = reverse('events', args=(self.date.strftime('%Y-%m-%d'),))
        return f'href="{url}"'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

