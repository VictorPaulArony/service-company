from django.shortcuts import render, redirect
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "main/home.html")

@login_required
def logout(request):
    django_logout(request)
    return redirect('main:home')
