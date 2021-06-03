from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import processor,ram,storage,gpu,powersupply,motherboard,cart,extendeduser,review
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.db.models import Subquery
from django.views.decorators.csrf import csrf_exempt
from pcparts.PayTm import Checksum

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')

def home(request):
    return render(request, "home.html")

def reviews(request):
    if request.method == 'POST':
        rev = str(request.POST['review'])
        a = str(request.session['category'])
        if 'id' in request.session:
            cid=request.session['id']
        user = User.objects.get(id=cid)
        firstname = str(user.first_name)
        pid=request.session['pid']
        r=review(cid=cid,cname=firstname,pid=pid,pcategory=a,review=rev)
        r.save()
        #redir=showproduct/pid
    return redirect('showproduct/'+str(pid))

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        specials = {'@','#','$','%','!'}
        if password1 == password2:
            if len(password1) < 7 or len(password1) > 20:
                messages.info(request, 'Weak Password !! \n Length of PASSWORD must be greater than 7 and less than 20')
                return redirect('register')
            flag = True
            if not any(char.isdigit() for char in password1): 
                # messages.info(request,'Password should have at least one numeral') 
                flag = False
            if not any(char.isupper() for char in password1): 
                # messages.info(request,'Password should have at least one uppercase letter')
                flag = False
            if not any(char.islower() for char in password1): 
                # messages.info(request,'Password should have at least one lowercase letter') 
                flag = False
            if not any(char in specials for char in password1): 
                # print('Password should have at least one of the symbols @#$%!') 
                flag = False
            if flag is False:
                messages.info(request, 'Weak Password !! Password must contain atleast one numeral, one alphabet and one special symbol(!,@,#,$,%)')
                return redirect('register')
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Mobile number Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'User Created')
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return redirect('register')
        return redirect('/')

    return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            request.session['id']=user.id
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request, 'login.html')

def myprofile(request):
    if 'id' in request.session:
        id=request.session['id']
        
        info=User.objects.filter(id=id)
        #request.session["mobile"]=User.objects.filter(id=id).values('username')
        info1 = extendeduser.objects.filter(cid=id)
        return render(request,'myprofile.html',{'info':info,'info1':info1})
    else:
        messages.info(request, 'you need to login')
        return redirect('login')

def forgot(request):
    return render(request, 'forgot_password.html')

def forgot_password(request):
    username = request.POST['user_name']
    request.session['forgot_user'] = username
    try:
        user = User.objects.get(username=username)
        email_id = user.email
        print(email_id)
        rno1 = random.randint(100000, 999999)
        request.session['OTP1'] = rno1
        msg = 'Your OTP For Password Reset is ' + str(rno1)
        send_mail('OTP for Password Reset', msg, 'pcpartsweb@gmail.com', [email_id], fail_silently=False)
        return render(request, 'forgot_otp.html')
    except user.DoesNotExist:
        messages.info(request, 'Invalid Username')
        return render(request, 'forgot_password.html')

def forgot_otp(request):
    otp1 = int(request.POST['otp1'])
    if otp1 == int(request.session['OTP1']):
        del request.session["OTP1"]
        # user = User.objects.get(username= request.session['forgot_user'])
        return render(request, 'set_password.html')
    else:
        messages.info(request, 'OTP verification Failed :(')
        return render(request, 'forgot_otp.html')

def set_passwords(request):
    new_pass = request.POST['pass2']
    user = User.objects.get(username=request.session['forgot_user'])
    user.password = make_password(new_pass)
    user.save(update_fields=['password'])
    user.save()
    messages.info(request, 'Password successfully reseted!!')
    return render(request, 'login.html')

def setsession(request,category):
    #info=image.objects.all()
    #return render(request,'serch.html',{'info' : info})
    #print('hello')
    #request.session['category']='{}'.format(category)
    #print('{}'.format(category))
    a='{}'.format(category)
    request.session['category'] = a
    #info=a.o
    #if request.session['category']=='Any':
    info=None
    if a == 'processor':
        info=processor.objects.all()
    elif a == 'ram':
        info=ram.objects.all()
    elif a == 'motherboard':
        info=motherboard.objects.all()
    elif a == 'storage':
        info=storage.objects.all()
    elif a == 'gpu':
        info=gpu.objects.all()
    elif a == 'powersupply':
        info=powersupply.objects.all()
    return render(request,'serch.html',{'info':info})
    # if request.session['category'] != 'Any':
    #     info=objects.filter(category = request.session['category'])
    #     return render(request,'serch.html',{'info':info})


def showproduct(request,myid):
    request.session['pid']=myid
    a = str(request.session['category'])
    info=None
    rev=review.objects.filter(pid=myid)
    if a == 'processor':
        info=processor.objects.filter(id=myid)
    elif a == 'ram':
        info=ram.objects.filter(id=myid)
    elif a == 'motherboard':
        info=motherboard.objects.filter(id=myid)
    elif a == 'storage':
        info=storage.objects.filter(id=myid)
    elif a == 'gpu':
        info=gpu.objects.filter(id=myid)
    elif a == 'powersupply':
        info=powersupply.objects.filter(id=myid)
    return render(request,'showproduct.html',{'info':info, 'rev':rev})

def addtocart(request):
    category=request.session['category']
    a=category
    request.session['category'] = category
    prod=request.POST['pid']
    catg=str(prod)
    catg=catg.split()
    category=catg[0]
    pid=str(catg[2])[1:-1]
    if a == 'processor':
        info=processor.objects.all()
    elif a == 'ram':
        info=ram.objects.all()
    elif a == 'motherboard':
        info=motherboard.objects.all()
    elif a == 'storage':
        info=storage.objects.all()
    elif a == 'gpu':
        info=gpu.objects.all()
    elif a == 'powersupply':
        info=powersupply.objects.all()
    if 'id' in request.session:
        cid=request.session['id']
        if category == 'processor':
            product1=processor.objects.filter(id=pid)
        elif category == 'ram':
            product1=ram.objects.filter(id=pid)
        elif category == 'motherboard':
            product1=motherboard.objects.filter(id=pid)
        elif category == 'storage':
            product1=storage.objects.filter(id=pid)
        elif category == 'gpu':
            product1=gpu.objects.filter(id=pid)
        elif category == 'powersupply':
            product1=powersupply.objects.filter(id=pid)
        for a in product1:
            print(a.name)
            name=a.name
            img=a.img
            desc=a.desc
            price=a.price
        t=cart(pid=pid,name=name,img=img,desc=desc,price=price,cid=cid,category=category)
        t.save()
        return render(request,'serch.html',{'info':info})
    else:
        messages.info(request, 'you need to login')
        return redirect('login')


def mycart(request):
    if 'id' in request.session:
        id=request.session['id']
        info=cart.objects.filter(cid=id)
        products = []
        totalPrice = 0
        for a in info:
            if a.category == 'processor' and id == a.cid:
                processor1=processor.objects.filter(id=a.pid)
                products.extend(processor1)
            elif a.category == 'ram' and id == a.cid:
                ram1=ram.objects.filter(id=a.pid)
                products.extend(ram1)
            elif a.category == 'storage' and id == a.cid:
                storage1=storage.objects.filter(id=a.pid)
                products.extend(storage1)
            elif a.category == 'motherboard' and id == a.cid:
                motherboard1=motherboard.objects.filter(id=a.pid)
                products.extend(motherboard1)
            elif a.category == 'powersupply' and id == a.cid:
                powersupply1=powersupply.objects.filter(id=a.pid)
                products.extend(powersupply1)
            elif a.category == 'gpu' and id == a.cid:
                gpu1=gpu.objects.filter(id=a.pid)
                products.extend(gpu1)
        # for a in info:
        #     totalPrice = totalPrice + a.price
        # print(totalPrice)
        return render(request,'mycart.html',{'products':products})
    else:
        messages.info(request, 'you need to login')
        return redirect('login')

def removeformcart(request):
    if 'id' in request.session:
        prod=request.POST['remove from cart']
        catg=str(prod)
        catg=catg.split()
        category=catg[0]
        pid=str(catg[2])[1:-1]
        id=request.session['id']
        info=cart.objects.filter(cid=id)
        for a in info:
            obj=cart.objects.filter(pid=pid,category=category)
            obj.delete()
            break
        return redirect('mycart')
    else:
        messages.info(request, 'you need to login')
        return redirect('login')

def updateprofileform(request):
    return render(request, 'updateprofile.html')

def updateprofile(request):
    id=request.session['id']
    user = User.objects.get(id=id)
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
       
        email = request.POST['email']

        
        if User.objects.filter(username=username ).filter(~Q(id=id)).exists() :
            messages.info(request, 'User already exists!!')
            return redirect('myprofile')
        elif User.objects.filter(email=email).filter(~Q(id=id)).exists():
            messages.info(request, 'Email already linked with other account')
            return redirect('myprofile')
        else:
            user.first_name = first_name
            user.save(update_fields=['first_name'])
            user.last_name = last_name
            user.save(update_fields=['last_name'])
            user.username = username
            user.save(update_fields=['username'])
            user.email = email
            user.save(update_fields=['email'])
            user.save()
        messages.info(request, 'You have successfully update profile!!')
        return redirect( 'myprofile')
    else:
        return render(request, 'updateprofile.html')

def search(request):
    info=None
    products = []
    if 'search' in request.GET:
        search=request.GET['search']
        if search == 'processor':
            info=processor.objects.all()
        elif search == 'ram':
            info=ram.objects.all()
        elif search == 'motherboard':
            info=motherboard.objects.all()
        elif search == 'storage':
            info=storage.objects.all()
        elif search == 'gpu':
            info=gpu.objects.all()
        elif search == 'powersupply':
            info=powersupply.objects.all()
    else:
        # processor1=processor.objects.all()
        # ram1=ram.objects.all()
        # motherboard1=motherboard.objects.all()
        # storage1=storage.objects.all()
        # gpu1=gpu.objects.all()
        # powersupply1=powersupply.objects.all()
        print('ccccccccccccccccc')
    return render(request,'serch.html',{'info':info})

def processorder(request):
    if request.method=="POST":
        return render(request, 'processorder.html')


def checkout(request):
    if request.method=="POST":
        id=request.session['id']
        email = request.POST.get('email', '')

        #amount = request.POST.get('amount', '')
        info=cart.objects.filter(cid=id)
        totalPrice=0
        for a in info:
            totalPrice = totalPrice + a.price
        print(totalPrice)
        amount = totalPrice
        print(email)
        MERCHANT_KEY = 'smy0Z3@3kS&ciqyT';
        param_dict = {

                'MID': 'zgUNxW31116401155231',
                # 'ORDER_ID': str(order.order_id),
                'ORDER_ID': '109',
                'TXN_AMOUNT': str(amount),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/pcparts/handlerequest/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'paytm.html', {'param_dict': param_dict})

    return render(request, 'checkout.html')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    return HttpResponse('done')
