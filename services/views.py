from django.shortcuts import render
# from django.http import HttpResponseRedirect

from users.models import Company

from .models import Service
# from .forms import CreateNewService, RequestServiceForm


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    return render(request, 'services/create.html', {})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    return render(request, 'services/request_service.html', {})


def company_list(request):
    companies = Company.objects.all()
    return render(request, 'users/company_list.html', {'companies': companies})
