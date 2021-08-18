import json
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from pathlib import Path
from .validator import *
from django.contrib import messages
from . import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import hmac
import hashlib
from django.core.mail import send_mail
from .OyeBot import OyeBot
from .proccess import Proccess_Data
import datetime
import random
# from OyeChatBot.app import proccess
# from app.proccess import Proccess_Data
# Create your views here.

BASE_DIR = Path(__file__).resolve().parent

print(BASE_DIR)

SECRET_KEY = bytes(settings.SECRET_KEY, 'utf-8')


def index(request):

    return render(request, 'index.html', context={'data': "response"})


def customerlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        fil_email = validate_email_field(email)
        if not fil_email['is_valid']:
            messages.error(request, fil_email['error'])

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            try:
                return redirect(request.GET.get('next'))
            except:
                return redirect('dashboard')
        else:
            messages.error(request, "Incorrect Email or Password")

    return render(request, 'auth/login.html')


def logOut(request):
    logout(request)
    messages.warning(request, "Logout Successfully")
    return redirect('login')


def signup(request):
    context = {}
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        val_name = validate_str_field(name, "Name")
        val_email = validate_email_field(email)
        val_username = validate_username_field(username, "Username")
        val_password = validate_password(password, "Password")

        if not val_name['is_valid']:
            messages.error(request, val_name['error'])
            return render(request, 'auth/register.html', context)

        if not val_email['is_valid']:
            messages.error(request, val_email['error'])
            return render(request, 'auth/register.html', context)

        if not val_username['is_valid']:
            messages.error(request, val_username['error'])
            return render(request, 'auth/register.html', context)

        if not val_password['is_valid']:
            messages.error(request, val_password['error'])
            return render(request, 'auth/register.html', context)

        try:
            user = User.objects.create_user(
                first_name=name, username=username, email=email, password=password)
            user.save()
        except Exception as e:
            messages.error(request, "Username Already Taken")
            return render(request, 'auth/register.html', context)
        otp = random.randint(000000, 999999)
        customer = models.Customers(
            user=user, email_otp=otp, email_verified=False, customer_status="inactive")
        customer.save()
        # subject = f"{otp} is the code for Email Verification"
        # message = f'''Hi {user.first_name},
        # You OTP for the email verification is {otp}
        # '''
        # mail = send_mail(subject=subject, message=message,
        #                  from_email="noreply@oyechatbot.com", recipient_list=[user.email], fail_silently=False)
        # if mail == 1:
        #     messages.success(request, "OTP sent on your email")
        #     return redirect('verifyOtp')
        # messages.error(
        #     request, "Unable to send OTP. Please try after some time")
        return redirect('addIntents')

    return render(request, 'auth/register.html', context)


def verify_email_with_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        a = User.objects.get(pk=request.user.id)
        user = models.Customers.objects.get(user__pk=request.user.id)
        if user:
            if user.email_otp == otp.strip():
                return redirect('dashboard')
    return render(request, 'auth/email_otp_verify.html')


# @login_required(login_url="login")
def dashboard(request):
    context = {}
    return render(request, 'dashboard/index.html', context)


def trainBot(request):
    allIntents = models.Intents.objects.all()
    data = {"intents": []}
    listData = []
    for intent in allIntents:
        result = {
            "tag": intent.tag,
            "patterns": intent.patterns.split('|'),
            "responses": intent.responses.split('|')
        }
        listData.append(result)
    data['intents'] = listData
    process = Proccess_Data(data)
    process.start_process()
    messages.success(request, "Dataset Trained Successfully")
    return redirect('addIntents')


# @login_required(login_url="login")
def addIntents(request):
    if request.method == 'POST':
        user = User.objects.get(email="akashdeep1@gmail.com")
        intents = json.loads(request.body.decode('utf-8'))
        patterns = intents['patterns']
        responses = intents['responses']
        # print(type(patterns))
        added_intent = models.Intents(
            customer=user, tag=intents['tag'], patterns=patterns, responses=responses)
        added_intent.save()
        allIntents = models.Intents.objects.values()
        # print(allIntents)
        return JsonResponse({"error": 0, "msg": "saved", "result": list(allIntents)}, safe=False)

    allIntents = models.Intents.objects.all()
    context = {"intents": allIntents}

    return render(request, 'dashboard/intents.html', context)


# @login_required(login_url="login")
def getMessage(request):
    if request.method == 'POST':
        req = json.loads(request.body.decode('utf-8'))
        ask = req['ask']
        allIntents = models.Intents.objects.all()
        data = {"intents": []}
        listData = []
        for intent in allIntents:
            result = {
                "tag": intent.tag,
                "patterns": intent.patterns.split('|'),
                "responses": intent.responses.split('|')
            }
            listData.append(result)
        data['intents'] = listData
        bot = OyeBot(data)
        print(ask)
        ans = bot.startChat(ask)
        context = {
            "error": 0,
            "result": ans
        }

        return JsonResponse(context, safe=False)
    return HttpResponse("mesase")
