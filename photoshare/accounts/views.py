from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
import base64
import qrcode
from io import BytesIO
from django.http import HttpResponse
from .models import *

def user_login (request):
    return render(request,'login.html')