from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.conf import settings
from urllib.parse import quote

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        phone_number = request.POST['phone_number']


        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please choose a different one.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')
        

        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        user.save()

        profile = UserProfile.objects.create(user=user,phone_number=phone_number)
        activation_key = profile.activation_key

        current_site = get_current_site(request)
        activation_url = f"{request.scheme}://{current_site.domain}/activate/{user.username}/{quote(activation_key)}"
        subject = 'Activate Your Account'
        message = 'Please click the link below to activate your account:\n\n{}'.format(activation_url)
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [email])


        return render(request, 'registration_success.html')
    else:
        return render(request, 'register.html')

def activate(request, username, token):
    user = User.objects.get(username = username)
    activation_obj = UserProfile.objects.get(user=user)
    if activation_obj.activation_key == token:
        activation_obj.is_active =True
        activation_obj.save()
        messages.success(request, 'Your account has been successfully activated.')
        return redirect('activation_success')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('home')


def activation_success(request):
    return render(request,'activation_success.html')



def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                active_check = UserProfile.objects.get(user=user)
                if active_check.is_active:
                    login(request, user)
                    messages.success(request, 'Successfully logged in.')
                    return redirect('dashboard') 
                else:
                    messages.warning(request, 'Your account is not active. Please check your email for verification instructions.')
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

        return render(request, 'login.html')

def user_logout(request):
    messages.success(request, 'Successfully logged out.')
    logout(request)
    return redirect('home')