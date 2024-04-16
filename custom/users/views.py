from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
import os,math,random,smtplib
from product.models import Product


    


@csrf_protect
def sign_in(request):
    
    if request.method =='GET':
        return render(request, 'login-register/login-registration.html')

    else:
        un = request.POST['uname']
        p = request.POST['upass']
        

        u = authenticate(username=un, password=p)
        #print(u)

        if u is not None:
            login(request, u)

            u1 = UserProfile.objects.filter(user = request.user)

            context = {}

            context['data1'] = u1

            return redirect("/index/")





def sign_up(request):
    context = {}
    
    if request.method == 'GET':
        return render(request, 'login-register/login-registration.html')

    elif request.method == 'POST':
        n = request.POST['name']
        un = request.POST['uname']
        p = request.POST['upass']
        cp = request.POST['ucpass']
        user_otp = request.POST.get('otp')  # Get OTP from POST data

        if n == '' or un == '' or p == '' or cp == '':
            context['errmsg'] = 'fields can not be blank'
            return render(request, 'login-register/login-registration.html', context)

        elif p != cp:
            context['errmsg'] = 'password and confirm password not match'
            return render(request, 'login-register/login-registration.html', context)

        elif len(p) < 8:
            context['errmsg'] = 'password must be 8 characters'
            return render(request, 'login-register/login-registration.html', context)

        else:
            try:
                u = User.objects.create(username=un)
                u.set_password(p)
                u.save()

                if u is not None:
                    pro = UserProfile.objects.create(user=u, name=n, email=un)
                    pro.save()
                    
                    # OTP Verification Code
                    digits = "0123456789"
                    OTP = ""
                    for i in range(6):
                        OTP += digits[math.floor(random.random() * 10)]
                    
                    otp_msg = OTP + " is your OTP"
                    
                    s = smtplib.SMTP('smtp.gmail.com', 587)
                    s.starttls()
                    s.login("prajwalwarhade07@gmail.com", "lkjp pldz bfmd jnon")
                    s.sendmail('&&&&&&&&&&&', un, otp_msg)
                    
                    if user_otp == OTP:  
                        context['success'] = 'Successfully registered and verified'
                        return render(request, 'login-register/login-registration.html', context)
                    else:
                        context['errmsg'] = 'Please Check your OTP again'
                        return render(request, 'login-register/login-registration.html', context)

                else:
                    context['errmsg'] = "Unfortunately, User Profile could not be created"
                    return render(request, 'login-register/login-registration.html', context)
            
            except Exception:
                context['errmsg'] = "User Already exists or an error occurred"
                return render(request, 'login-register/login-registration.html', context)

            
def user_logout(request):
    logout(request)
    return redirect('sign_up')

def index(request):
    u=None
    if request.user.is_authenticated:
        u = UserProfile.objects.filter(user = request.user)
    
    p = Product.objects.filter(is_active=True) # for product show in index file 
    context = {
        'prod': p,
        'data1':u
        }
    return render(request,'index.html', context)

def profile(request):
    pro = UserProfile.objects.filter(user = request.user)
    u = UserProfile.objects.filter(user = request.user)
    context = {
        'data' : pro,
        'data1' : u
    }
    return render (request, 'profile.html',context)

