from django.shortcuts import render

# Create your views here.
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import *
from django.template.context_processors import csrf
from django.views.decorators.cache import cache_control
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'User already exists!!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already linked with other account')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()

        else:
            messages.info(request, 'Password is not matching')
            return redirect('register')
        messages.info(request, 'You have successfully signed up!!')
        return render(request, 'login.html')
    else:
        return render(request, 'register.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            request.session["username"]=username
            auth.login(request,user)
            info=User.objects.get(username=username)
            request.session['cid']=info.id
            #return HttpResponse(request.session['cid'])
            return redirect('homepage')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
def homepage(request):
    request.session['category']="Any"
    request.session['city']="Any"
    return render(request, 'home.html')
def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out!!')
    return render(request, 'login.html')
def forgot(request):
    return render(request, 'forgot_password.html')
def forgot_password(request):
    username = request.POST['user_name']
    request.session['forgot_user'] = username
    try:
        user = User.objects.get(username=username)
        email_id = user.email
        rno1 = random.randint(100000, 999999)
        request.session['OTP1'] = rno1
        msg = 'Your OTP For Password Reset is ' + str(rno1)
        send_mail('OTP for Password Reset',
                  msg,
                  'soldold765@gmail.com',
                  [email_id],
                  fail_silently=False)
        return render(request, 'forgot_otp.html')
    except User.DoesNotExist:
        messages.info(request, 'Invalid Username')
        return render(request, 'forgot_password.html')
def otp_verification1(request):
    otp1 = int(request.POST['otp1'])
    if otp1 == int(request.session['OTP1']):
        del request.session["OTP1"]
        # user = User.objects.get(username= request.session['forgot_user'])
        return render(request, 'set_password.html')
    else:
        messages.info(request, 'OTP verification Failed:(')
        return render(request, 'forgot_otp.html')
def set_passwords(request):
    new_pass = request.POST['pass2']
    user = User.objects.get(username=request.session['forgot_user'])
    user.password = make_password(new_pass)
    user.save(update_fields=['password'])
    user.save()
    messages.info(request, 'Password successfully reseted!!')
    return render(request, 'login.html')



