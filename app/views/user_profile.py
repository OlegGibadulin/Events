from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
import django.contrib.auth as auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from app.models import UserProfile
from app.forms import RegisterForm, LoginForm

def register(request):
    form = RegisterForm(request.POST or None)

    if request.POST and form.is_valid():
        # form.register()
        form.save()
        user = form.get_user()
        auth.login(request, user)
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'form.html', {'form': form})

def login(request):
    redirected_path = request.GET.get('next', '/')
    form = LoginForm(request.POST or None)

    if request.POST and form.is_valid():
        user = form.get_user()
        auth.login(request, user)
        return redirect(redirected_path)
    return render(request, 'form.html', {'form': form})

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

