from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import register_customer, register_company, login_view, home

urlpatterns = [
    path('', home, name='home'),
    path('company/',register_company , name='register_company'),
    path('customer/', register_customer, name='register_customer'),
    path('login/', login_view, name='login'),
     path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
