from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

from app.models import Event, Patient
from app.forms import EventForm

def handle_create_form(request, form):
    if 'term' in request.GET:
        pattern = request.GET.get('term')
        medications = Event.objects.medication_list(pattern)
        return JsonResponse(medications, safe=False)
    
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'create_form.html', {'form': form})

@login_required(login_url='/login')
def create_event(request, eid=None):
    instance = Event() if not eid else get_object_or_404(Event, pk=eid)
    form = EventForm(request.POST or None, instance=instance)
    return handle_create_form(request, form)

@login_required(login_url='/login')
def create_event_on_date(request, date):
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'date': date})
    return handle_create_form(request, form)

@login_required(login_url='/login')
def create_event_on_patient(request, pid):
    patient = Patient.objects.get(pk=pid)
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'patient': patient})
    return handle_create_form(request, form)

@login_required(login_url='/login')
def edit_event(request, eid=None):
    instance = Event() if not eid else get_object_or_404(Event, pk=eid)
    form = EventForm(request.POST or None, instance=instance)
    
    if 'term' in request.GET:
        pattern = request.GET.get('term')
        medications = Event.objects.medication_list(pattern)
        return JsonResponse(medications, safe=False)
    
    if request.POST:
        if 'delete' in request.POST:
            Event.objects.delete(eid)
            return HttpResponseRedirect(reverse('calendar'))
        elif 'save' in request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'edit_form.html', {'form': form})

@login_required(login_url='/login')
def events(request, date):
    context = {
        'events': Event.objects.by_date(date),
        'date': date,
    }
    return render(request, 'events.html', context)
