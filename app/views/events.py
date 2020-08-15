from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from datetime import datetime
from django.contrib.auth.decorators import login_required

from app.models import Event, Patient
from app.forms import EventForm

@login_required(login_url='/login')
def edit_event(request, eid=None):
    instance = Event() if not eid else get_object_or_404(Event, pk=eid)
    form = EventForm(request.POST or None, instance=instance)

    if 'term' in request.GET:
        pattern = request.GET.get('term')
        medications = Event.objects.medication_list(pattern)
        return JsonResponse(medications, safe=False)
    
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def event_on_date(request, date):
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'date': date})
    
    if 'term' in request.GET:
        pattern = request.GET.get('term')
        medications = Event.objects.medication_list(pattern)
        return JsonResponse(medications, safe=False)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def event_on_patient(request, pid):
    patient = Patient.objects.get(pk=pid)
    instance = Event()
    form = EventForm(request.POST or None, instance=instance, initial={'patient': patient})

    if 'term' in request.GET:
        pattern = request.GET.get('term')
        medications = Event.objects.medication_list(pattern)
        return JsonResponse(medications, safe=False)

    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def events(request, date):
    context = {
        'events': Event.objects.by_date(date),
        'date': date,
    }
    return render(request, 'events.html', context)
