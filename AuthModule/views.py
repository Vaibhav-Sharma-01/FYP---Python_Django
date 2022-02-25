from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from AuthModule.models import user
from django.utils import timezone


def index(request):
    return render(request, 'auth/Login_SignUp.html')


def login(request):
    email = request.POST.get('email', 'default')
    password = request.POST.get('password', 'default')
    users = user.objects.get(email=email, password=password)
    if(users):
        return HttpResponseRedirect('home')
        # return render(request, 'home/HomePage.html')


def signup(request):
    username = request.POST.get('uname', 'default')
    email = request.POST.get('email', 'default')
    password = request.POST.get('password', 'default')
    users = user(username=username, email=email,
                 password=password, created_date=timezone.now())
    print(users)
    users.save()
    return HttpResponse("sign up successfull")
