from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.template.loader import render_to_string

from app.models import Procedure, Event
from app.forms import ProcedureForm

@login_required(login_url='/login')
def procedures(request):
    context = {
        'procedures': Procedure.objects.newest(),
        'events': Event.objects.all(),
    }
    return render(request, 'procedures.html', context)

@login_required(login_url='/login')
def edit_procedure(request, pid=None):
    instance = Procedure() if not pid else get_object_or_404(Procedure, pk=pid)
    form = ProcedureForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('procedures'))
    return render(request, 'form.html', {'form': form})

@login_required(login_url='/login')
def filter_procedures(request):
    procedure_title = request.GET.get('procedure_title', None)
    events = Event.objects.by_procedure(procedure_title)
    html = render_to_string('inc/events.html', {'events': events})
    # print(events)
    # data = serializers.serialize("json", events)
    # return JsonResponse(data, safe=False)
    return HttpResponse(html)
