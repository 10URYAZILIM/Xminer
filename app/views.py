from django.shortcuts import render,HttpResponse,redirect,render_to_response
from .forms import UpdateUserForm
from .models import User,machine,news,user_machine,user_machine_log,TheMachineGain
from django.contrib.auth import logout
import datetime
from django.utils import timezone
from django.db import connection



def home(request):
    return render(request,'index.html')

def index(request):
    if not request.user.is_authenticated:
        return redirect('home')
    user_payment(request)
    ## HABERLERİ ÇEKELİM
    haberler=news.objects.all().order_by('-id')[:4]
    ## KULLANICININ CİHAZLARINI ÇEKELİM
    machines=user_machine.objects.raw("SELECT usmac.id,usmac.miner_power,COUNT(machine_id) as Adet,mac.model,mac.image,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s AND usmac.machine_dead>=%s GROUP BY  usmac.machine_id ORDER BY Adet DESC ",[request.user.id,timezone.now()])
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista=cihaz_istatistik(request)
    context = {
        'link': 'index',
        'haberler':haberler,
        'machines':machines,
        'cihaz_istatistik':cihaz_ista,
        'machine_count':len(list(machines))
    }
    return render(request,'app/index.html',context)

def user(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## UPDATE FORMUNU OLUŞTURALIM
    form=UpdateUserForm(instance=request.user)
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    context={
        'link':'user',
        'form':form,
        'cihaz_istatistik':cihaz_ista
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
    cihaz_ista = cihaz_istatistik(request)
    context={
        'link':'market',
        'machines':machines,
        'cihaz_istatistik':cihaz_ista

    }
    return  render(request,'app/market.html',context)


def store(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## Kullanıcının Tüm Makinelerini Çağıralım
    user_id=request.user.id
    usermachines=User.objects.raw('select usmac.id,usmac.date,usmac.miner_power,usmac.fiyat,usmac.machine_dead,model,user_id,mac.miner_power_rate FROM app_user_machine as usmac INNER JOIN app_machine as mac on mac.id=usmac.machine_id WHERE usmac.user_id=%s',[user_id])
    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    zaman=timezone.now()
    context={
        'link':'store',
        'usermachines':usermachines,
        'cihaz_istatistik':cihaz_ista,
        'zaman':zaman
    }
    return render(request,'app/store.html',context)

def report(request):
    if not request.user.is_authenticated:
        return redirect('home')

    ## KULLANININ TOPLAM HASH RATE
    cihaz_ista = cihaz_istatistik(request)
    zaman=timezone.now()
    context={
        'link':'report',
        'cihaz_istatistik':cihaz_ista,
        'zaman':zaman
    }
    return render(request,'app/report.html',context)

def cihaz_istatistik(request):
    print ("---------",timezone.now())
    rows=request.user.usermachine.all().filter(machine_dead__gte=timezone.now())
    mh=0
    th=0
    gh=0
    makine_count=rows.count
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
    return {'mh':mhh,'th':thh,'gh':ghh,'cihazlar':rows,'makine_count':makine_count}

def user_payment(request):
    cursor=connection.cursor()
    ## KULLANICININ ÖDENMEMİŞ CİHAZLARINI ÇEKELİM
    zaman=timezone.now()-datetime.timedelta(days=1)
    print ('ZAMAN: ',zaman)
    odeme_tutari=0
    UserMac=user_machine_log.objects.filter(date__lte=zaman,payment=False,user_id=request.user.id)

    for i in range(0,len(UserMac)): ## Ödeme Alacak Cihazları dönelim
        gecen_zaman=(timezone.now()-UserMac[i].date).days
        print ("Geçen Zaman: ",gecen_zaman)
        ## GEÇEN ZAMANI LOG KAYITLARINA TEK TEK EKLEYELİM
        for gun in range(0,gecen_zaman):
            # Geçen Zaman Hangi gün ödeme olucak
            odeme_gunu=UserMac[i].date+datetime.timedelta(days=gun)
            print ("Ödeme Günü: ",odeme_gunu)

            TheMachine=TheMachineGain.objects.filter(date__lte=odeme_gunu)[:1]
            print (TheMachine[0].gain)


            ## USERLOG ÖDEMESİ ALINDI GÜNCELLE
            #cursor.execute("UPDATE app_user_machine_log SET payment=%s,pay=%s WHERE date=%s AND user_id=%s AND user_machine_id=%s",[True,10,odeme_gunu,request.user.id,UserMac[i].user_machine_id])
            ## USERLOG 1 Gün Sonrasını kayıt edelim
            UserLog=user_machine_log()
            UserLog.date=(odeme_gunu+datetime.timedelta(days=1))
            UserLog.machine_dead=UserMac[i].machine_dead
            UserLog.machine_id=UserMac[i].machine_id
            UserLog.user_id=UserMac[i].user_id
            UserLog.user_machine_id=UserMac[i].user_machine_id
            #UserLog.save()
