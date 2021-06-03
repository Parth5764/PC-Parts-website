from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$',views.login,name='login'),
    path('',views.homepage),
    url(r'^homepage/$',views.homepage,name='homepage'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^forgot_password/$',views.forgot_password,name='forgot_password'),
    url(r'^otp_verification1/$',views.otp_verification1,name='otp_verification1'),
    url(r'^set_passwords/$',views.set_passwords,name='set_passwords'),
    url(r'^forgot/$',views.forgot,name='forgot'),

]