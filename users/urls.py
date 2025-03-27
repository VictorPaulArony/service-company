from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    register,
    CustomerSignUpView,
    CompanySignUpView,
    LoginUserView,
)

urlpatterns = [
    path('', register, name='register'),
    path('customer/', CustomerSignUpView.as_view(), name='register_customer'),
    path('company/', CompanySignUpView.as_view(), name='register_company'),
    path('login/', LoginUserView, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
