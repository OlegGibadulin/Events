from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from app.models import Event, Patient
from app.forms import EventForm

def edit_event(request, eid=None):
    instance = Event() if not eid else get_object_or_404(Event, pk=eid)
    form = EventForm(request.POST or None, instance=instance)
    
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

def event_on_date(request, date):
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'date': date})

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

def event_on_patient(request, pid):
    patient = Patient.objects.get(pk=pid)
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'patient': patient})

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

def events(request, date):
    context = {
        'events': Event.objects.by_date(date),
        'date': date,
    }
    return render(request, 'events.html', context)
