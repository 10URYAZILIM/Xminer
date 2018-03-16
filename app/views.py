from django.shortcuts import render,HttpResponse,redirect,render_to_response
from .forms import UpdateUserForm
from .models import User,machine,news,user_machine
from django.contrib.auth import logout



def home(request):
    return render(request,'index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## HABERLERİ ÇEKELİM
    haberler=news.objects.all().order_by('-id')[:4]
    ## KULLANICININ CİHAZLARINI ÇEKELİM
    machines=user_machine.objects.raw("SELECT usmac.id,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_id,usmac.machine_dead,COUNT(machine_id) as Adet,mac.model,mac.image,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s GROUP BY  usmac.machine_id ORDER BY Adet DESC ",[request.user.id])
    ## KULLANININ TOPLAM HASH RATE
    toplam_hash=toplam_hash_rate(request)
    context = {
        'link': 'index',
        'haberler':haberler,
        'machines':machines,
        'toplam_hash':toplam_hash,
        'machine_count':len(list(machines))
    }
    return render(request,'app/index.html',context)

def user(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## UPDATE FORMUNU OLUŞTURALIM
    form=UpdateUserForm(instance=request.user)
    ## KULLANININ TOPLAM HASH RATE
    toplam_hash = toplam_hash_rate(request)
    context={
        'link':'user',
        'form':form,
        'toplam_hash':toplam_hash
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
    ## KULLANININ TOPLAM HASH RATE
    toplam_hash = toplam_hash_rate(request)
    context={
        'link':'market',
        'machines':machines,
        'toplam_hash':toplam_hash

    }
    return  render(request,'app/market.html',context)


def store(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## Kullanıcının Tüm Makinelerini Çağıralım
    user_id=request.user.id
    usermachines=User.objects.raw('select usmac.id,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_dead,model,user_id,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s',[user_id])
    ## KULLANININ TOPLAM HASH RATE
    toplam_hash = toplam_hash_rate(request)
    context={
        'link':'store',
        'usermachines':usermachines,
        'toplam_hash':toplam_hash
    }
    return render(request,'app/store.html',context)





def toplam_hash_rate(request):
    rows=request.user.usermachine.all()
    mh=0
    th=0
    gh=0
    for row in rows:
        if row.miner_power_rate=='TH':
            th=float(th)+float(row.miner_power)
        elif row.miner_power_rate=='GH':
            gh= float(gh)+float(row.miner_power)
        else:
            mh=float(mh)+float(row.miner_power)
    thh=float(th)+float(float(gh)/1000)+(float(mh)/1000000)
    ghh=float(gh)+float(float(mh)/1000)+(float(th)*1000)
    mhh=float(mh)+float(float(gh)*1000)+(float(th)*1000000)
    return {'mh':mhh,'th':thh,'gh':ghh}
