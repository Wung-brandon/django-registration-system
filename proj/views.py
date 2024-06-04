from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user = auth.authenticate(username=username, email=email)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successfully')
            return redirect('user')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

def user(request):
    user = User.objects.all()
    context = {
        'user': user,
    }
    return render(request, 'user.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            user_exists = User.objects.filter(username=username).exists()
            email_exists = User.objects.filter(email=email).exists()
            if user_exists:
                messages.info(request, 'User with username already exists')
                return redirect('register')
            elif email_exists:
                messages.info(request, 'User with email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.info(request, 'Password Mismatch')
    else:
        return render(request, 'register.html')


