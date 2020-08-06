from django.db import models
from django.urls import reverse
from django.utils import timezone

from app.managers import PatientManager

class Patient(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    is_active = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now, db_index=True)

    objects = PatientManager()

    def __str__(self):
        return '{}'.format(self.name)

class Procedure(models.Model):
    title = models.CharField(max_length=200)
    ref_num = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.title, self.ref_num)

class Event(models.Model):
    date = models.DateTimeField()
    price = models.PositiveIntegerField(default=0)

    procedures = models.ManyToManyField(Procedure, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)

    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.id} </a>'

