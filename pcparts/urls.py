from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('reviews', views.reviews, name='reviews'),
    path('login', views.login, name='login'),
    path('home', views.home, name='home'),
    path('logout', views.logout, name='logout'),
    path('forgot', views.forgot, name='forgot'),
    #path('set_passwords', views.set_passwords,name='set_passwords'),
    path('setsession/<category>', views.setsession),
    path('search', views.search, name='search'),
    path('forgot_otp', views.forgot_otp, name='forgot_otp'),
    path('addtocart',views.addtocart,name='addtocart'),
    path('showproduct/<int:myid>/',views.showproduct,name='showproduct'),
    path('mycart', views.mycart,name='mycart'),
    path('removeformcart',views.removeformcart,name='removeformcart'),
    path('set_passwords', views.set_passwords, name='set_passwords'),
    path('forgot_password', views.forgot_password, name='forgot_password'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('updateprofileform',views.updateprofileform,name='updateprofileform'),
    path('updateprofile',views.updateprofile,name='updateprofile'),
    path('processorder',views.processorder,name='processorder'),
    path('checkout',views.checkout,name='checkout'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('', views.home, name="home"),
]
