from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns =[
    path('register-customer/',views.register_customer,name='register-customer'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout')
]