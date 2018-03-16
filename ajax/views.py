from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login as dj_login,authenticate
from app.forms import *
import json
import requests
import datetime
from django.contrib.auth.hashers import check_password

def borsa_cek(request):
    r = requests.get('http://bitfindeks.com/rest/ticker/apiV1')
    borsa=r.json()
    eth=borsa[13]["coinRate"]
    btc=borsa[17]["coinRate"]
    ltc=borsa[26]["coinRate"]
    xrp=borsa[72]["coinRate"]
    return HttpResponse(json.dumps({'allborsa':borsa,'eth':eth,'btc':btc,'ltc':ltc,'xrp':xrp}),content_type="application/json")

def login(request):
    if request.is_ajax():
        form=LoginForm(request.POST or None)
        if form.is_valid():
            ## Giriş Başarılı Oturumu başlatalım
            dj_login(request,form.user)
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')


def update_user(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdateUserForm(request.POST or None,instance=request.user)
        if form.is_valid():
            update=form.save(commit=False)
            update.user=request.user
            update.save()
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def update_password(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdatePasswordForm(request.POST or None,user=request.user)
        if form.is_valid():
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')

def update_avatar(request):
    if request.is_ajax() and request.user.is_authenticated:
        form=UpdateAvatarForm(request.POST or None, request.FILES or None,instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse(json.dumps({'durum': 1}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({'durum':0,'mesaj':form.errors}),content_type="application/json")
    else:
        return redirect('home')