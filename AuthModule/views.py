from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from AuthModule.models import user
from django.utils import timezone
from django.contrib import messages

def index(request):
    return render(request, 'auth/Login_SignUp.html')


def login(request):
    email = request.POST.get('email', 'default')
    password = request.POST.get('password', 'default')
    try:
        users = user.objects.get(email=email, password=password)
        if(users):
            return HttpResponseRedirect('home')
    except Exception:
        messages.info(request, 'Login Error!!')
        messages.info(request, 'Invalid email or password.')
        return render(request, 'auth/Login_SignUp.html')
        # return render(request, 'home/HomePage.html')


def signup(request):
    username = request.POST.get('uname', 'default')
    email = request.POST.get('email', 'default')
    password = request.POST.get('password', 'default')
    try:
        user.objects.get(email=email)
        messages.info(request, 'SignUp Error!!')
        messages.info(request, 'User Already Exists!!')
    except Exception:
        users = user(username=username, email=email,
                 password=password, created_date=timezone.now())
        users.save()
        messages.info(request, 'SignUp Successfull!!')
    return render(request, 'auth/Login_SignUp.html')
