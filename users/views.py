from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from django.views.generic import CreateView, TemplateView

from .forms import CustomerSignUpForm, CompanySignUpForm, LoginForm
from .models import User, Company, Customer


#view of the customer registration 
def register_customer(request):
    if request.Method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = user.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                is_customer=True
            )
            Customer.objects.create(user=user, date_of_birth=form.cleaned_data['date_of_birth'])
            return redirect('login')
        else:
          form = CustomerSignUpForm()
    return render(request, 'register_customer.html', {'form': form})  

#view for the company registration 
def register_company(request):
    if request.method == "POST":
        form = CompanySignUpForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                email=form.cleaned_data['email'],
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                is_company=True
            )
            Company.objects.create(user=user, field_of_work=form.cleaned_data['field_of_work'])
            return redirect('login')
    else:
        form = CompanySignUpForm()
    return render(request, 'register_company.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def home(request):
    return render(request, 'home.html')
