from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from datetime import datetime

from app.models import Event
from app.forms import EventForm

def event(request, eid=None):
    # instance = Patient() if not pid else get_object_or_404(Patient, pk=pid)
    instance = Event()
    if eid:
        instance = get_object_or_404(Event, pk=eid)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event.html', {'form': form})

def event_on_date(request, date):
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'date': date})

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'event.html', {'form': form})

def events(request, date):
    # date = datetime.strptime(date, '%Y-%m-%d')
    context = {
        'events': Event.objects.by_date(date)
    }
    return render(request, 'events.html', context)
