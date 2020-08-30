from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers

from app.models import Procedure, Event, UserProfile
from app.forms import ProcedureForm

@login_required(login_url='/login')
def procedures(request):
    context = {
        'procedures': Procedure.objects.newest(request.user),
        'events': Event.objects.newest(request.user),
    }
    return render(request, 'procedures.html', context)

@login_required(login_url='/login')
def create_procedure(request):
    instance = Procedure()
    form = ProcedureForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        procedure = form.save(commit=False)
        procedure.author = UserProfile.objects.by_user(request.user)
        procedure.save()
        return HttpResponseRedirect(reverse('procedures'))
    return render(request, 'create_form.html', {'form': form})

@login_required(login_url='/login')
def edit_procedure(request, pid):
    instance = Procedure() if not pid else get_object_or_404(Procedure, pk=pid)
    form = ProcedureForm(request.POST or None, instance=instance)
    if request.POST:
        if 'delete' in request.POST:
            Procedure.objects.delete(pid)
            return HttpResponseRedirect(reverse('procedures'))
        elif 'save' in request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('procedures'))
    return render(request, 'edit_form.html', {'form': form})

@login_required(login_url='/login')
def procedure(request, pid):
    procedure = Procedure.objects.get(pk=pid)
    events = Event.objects.by_procedure(pid, request.user)
    context = {
        'procedure': procedure,
        'events': events,
    }
    return render(request, 'procedure.html', context)
