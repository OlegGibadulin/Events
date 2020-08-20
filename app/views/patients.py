from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from app.models import Patient, Event
from app.forms import PatientForm

@login_required(login_url='/login')
def patients(request):
    return render(request, 'patients.html')

@login_required(login_url='/login')
def create_patient(request):
    instance = Patient()
    form = PatientForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('patients'))
    return render(request, 'create_form.html', {'form': form})

@login_required(login_url='/login')
def edit_patient(request, pid):
    instance = Patient() if not pid else get_object_or_404(Patient, pk=pid)
    form = PatientForm(request.POST or None, instance=instance)
    if request.POST:
        if 'delete' in request.POST:
            Patient.objects.delete(pid)
            return HttpResponseRedirect(reverse('patients'))
        elif 'save' in request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('patients'))
    return render(request, 'edit_form.html', {'form': form})

@login_required(login_url='/login')
def patient(request, pid):
    patient = Patient.objects.get(pk=pid)
    events = Event.objects.by_patient(pid)
    context = {
        'patient': patient,
        'events': events,
    }
    return render(request, 'patient.html', context)

@login_required(login_url='/login')
def search_patients(request):
    search_request = request.GET.get('search_request', None)
    patients = Patient.objects.starts_with(search_request)
    html = render_to_string('inc/patients.html', {'patients': patients})
    return HttpResponse(html)
