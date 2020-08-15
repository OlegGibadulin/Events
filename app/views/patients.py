from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from app.models import Patient, Event
from app.forms import PatientForm

@login_required(login_url='/login')
def patients(request):
    context = {
        'patients': Patient.objects.newest(),
    }
    return render(request, 'patients.html', context)

@login_required(login_url='/login')
def edit_patient(request, pid=None):
    instance = Patient() if not pid else get_object_or_404(Patient, pk=pid)
    form = PatientForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('patients'))
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def patient(request, pid):
    patient = Patient.objects.get(pk=pid)
    events = Event.objects.by_patient(pid)
    context = {
        'patient': patient,
        'events': events,
    }
    return render(request, 'patient.html', context)