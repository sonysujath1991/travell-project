from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import place
from .models import team


# Create your views here.

def home(request):
    obj = place.objects.all
    obj1 = team.objects.all
    return render(request, "index.html", {'result': obj, 'result1': obj1})


def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        em = request.POST['email']
        psw = request.POST['psw']
        cpsw = request.POST['psw-repeat']

        if psw == cpsw:
            if User.objects.filter(username=uname).exists():
                messages.info(request, "username already Taken")
                print("username already exists")
                return redirect('register')

            elif User.objects.filter(email=em).exists():
                messages.info(request, "email already exists")
                print("email already used")
                return redirect('register')
            else:
                user = User.objects.create_user(username=uname, first_name=fname, last_name=lname, email=em,
                                                password=psw)
                user.save()
                print("user created")
                return redirect('login')

        else:
            print("password not matching")
            messages.info(request, "password not matching")
            return redirect('register')
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')

        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
