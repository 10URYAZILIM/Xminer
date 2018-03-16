from django.shortcuts import render,HttpResponse,redirect,render_to_response
from .forms import UpdateUserForm
from .models import User
from django import template

register = template.Library()
@register.filter( takes_context=True)
def cutt(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')

def home(request):
    return render(request,'index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    context = {
        'link': 'index'
    }
    return render(request,'app/index.html',context)

def user(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## UPDATE FORMUNU OLUŞTURALIM
    form=UpdateUserForm(instance=request.user)
    context={
        'link':'user',
        'form':form
    }
    return  render(request,'app/user.html',context)

def market(request):
    if not request.user.is_authenticated:
        return redirect('home')


    context={
        'link':'market',

    }
    return  render(request,'app/market.html',context)


def store(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## Kullanıcının Tüm Makinelerini Çağıralım
    user_id=request.user.id
    usermachines=User.objects.raw('select usmac.id,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_dead,model,user_id FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s',[user_id])
    context={
        'link':'store',
        'usermachines':usermachines
    }
    return render(request,'app/store.html',context)




