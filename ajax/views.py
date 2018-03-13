from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login as dj_login,authenticate
from app.forms import *
import json

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
