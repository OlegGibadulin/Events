from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from app.models import Procedure
from app.forms import ProcedureForm

def procedures(request):
    context = {
        'procedures': Procedure.objects.newest(),
    }
    return render(request, 'procedures.html', context)

def edit_procedure(request, pid=None):
    instance = Procedure() if not pid else get_object_or_404(Procedure, pk=pid)
    form = ProcedureForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('procedures'))
    return render(request, 'form.html', {'form': form})
