from django.shortcuts import render,HttpResponse,redirect,render_to_response
from .forms import UpdateUserForm
from .models import User,machine,news,user_machine
from django import template
from django.contrib.auth import logout

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

    ## HABERLERİ ÇEKELİM
    haberler=news.objects.all().order_by('-id')[:4]
    ## KULLANICININ CİHAZLARINI ÇEKELİM
    machines=user_machine.objects.raw("SELECT usmac.id,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_id,usmac.machine_dead,COUNT(machine_id) as Adet,mac.model,mac.image FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s GROUP BY  usmac.machine_id ORDER BY Adet DESC ",[request.user.id])
    context = {
        'link': 'index',
        'haberler':haberler,
        'machines':machines,
        'machine_count':len(list(machines))
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
def user_logout(request):
    logout(request)
    return redirect('home')
def market(request):
    if not request.user.is_authenticated:
        return redirect('home')
    ## Tüm Makineleri Çağırılam
    machines=machine.objects.all()
    context={
        'link':'market',
        'machines':machines

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



