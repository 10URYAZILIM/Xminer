from django import forms
from .models import User,machine,user_machine,user_machine_log,Payment
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.utils import timezone
import datetime

## FORM İÇİN GEREKLİ ARAÇ FONKSYİONLARI
def AddYear(date, years):
    result = date + datetime.timedelta(366 * years)
    if years > 0:
        while result.year - date.year > years or date.month < result.month or date.day < result.day:
            result += datetime.timedelta(-1)
    elif years < 0:
        while result.year - date.year < years or date.month > result.month or date.day > result.day:
            result += datetime.timedelta(1)
    return result

#######

##############################################################3
## KULLANICI LOGIN FORMU
class LoginForm(forms.ModelForm):
    user=None
    class Meta:
        model=User
        fields=('username','password')
    def clean(self):
        kullanici_adi=self.cleaned_data.get("username")
        sifre=self.cleaned_data.get("password")
        if kullanici_adi and sifre:
            self.user=authenticate(username=kullanici_adi,password=sifre)
            if self.user is None:
                # Kullanıcı adı veya şifre yanlış
                raise forms.ValidationError("Kullanıcı Adı veya Şifre Hatalı !")
        else:
            raise forms.ValidationError("Boş Bırakmayınız !")
##############################################################3
## KULLANICI BİLGİLERİNİ GÜNCELLEME FORMU
class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'first_name','last_name','tel','tc_no','email'
        ]

    def clean(self):
        first_name=self.cleaned_data.get("first_name")
        last_name=self.cleaned_data.get("last_name")
        tel=self.cleaned_data.get("tel")
        tc_no=self.cleaned_data.get("tc_no")
        email=self.cleaned_data.get("email")

        if first_name and last_name and tel and tc_no and email:
            if len(tel)<15:
                raise forms.ValidationError("Telefon Numarasınızı Doğru Giriniz")
        else:
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")

##############################################################3
### KULLANICI ŞİFRE DEĞİŞTİRME FORMU
class UpdatePasswordForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(UpdatePasswordForm, self).__init__(*args,**kwargs)
    new_password=forms.CharField(max_length=40,required=False)
    new_password2=forms.CharField(max_length=40,required=False)
    class Meta:
        model=User
        fields=[
            'password'
        ]

    def clean(self):
        new_password=self.cleaned_data.get("new_password")
        new_password2=self.cleaned_data.get("new_password2")
        password=self.cleaned_data.get("password")
        if new_password and new_password2 and password:
            if new_password!=new_password2:
                raise forms.ValidationError("Yeni Şifreniz Tekrarı İle Uyuşmuyor")
            else:
                if not self.user.check_password(password):
                    raise forms.ValidationError("Şifrenizi Yanlış Girdiniz !")
                else:
                    self.user.set_password(new_password)
                    self.user.save()
        else:
            raise forms.ValidationError("Tüm Alanları Doldurun !")

##############################################################3
## KULLANICI FOTOĞRAF DEĞİŞTİRME FORMU
class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'avatar'
        ]


##############################################################3
## CİHAZ SATIN ALMA FORMU
class MachineBuyForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(MachineBuyForm, self).__init__(*args,**kwargs)

    machineid=forms.IntegerField(required=False)

    def clean(self):
        MachineId=self.cleaned_data.get('machineid')
        ## Bu makina Varmı kontol edelim
        Mac=machine.objects.filter(id=MachineId)
        print ("POST :",MachineId)
        if Mac:
            ## MACHİNE MEVCUT
            ## BAKİYE KONTROL
            if self.user.hesap>Mac[0].fiyat:
                ## BAKİYE VAR BAKİYEDEN EKSİLTİP CİHAZI SATIN ALALIM
                self.user.hesap=self.user.hesap-Mac[0].fiyat
                self.user.save()
                ## BAKİYEDEN DÜŞTÜK ŞİMDİ KULLANICIIN MAKİNELER TABLOSUNA VE LOG TABLOSUNA BUNLARI EKLEYEK
                UserMac=user_machine()
                UserMac.fiyat=Mac[0].fiyat
                UserMac.user_id=self.user.id
                UserMac.machine_id=Mac[0].id
                UserMac.miner_power=Mac[0].miner_power
                UserMac.miner_power_rate=Mac[0].miner_power_rate
                UserMac.date=timezone.now()
                machine_dead=AddYear(timezone.now(),Mac[0].lifetime)
                UserMac.machine_dead=machine_dead
                UserMac.save()
                ## Kullanının Makinesi Tanımlandı Şimdi loga atalım
                UserMacLog=user_machine_log()
                UserMacLog.machine_id=Mac[0].id
                UserMacLog.user_machine_id=UserMac.id
                UserMacLog.date=timezone.now()
                UserMacLog.machine_dead=machine_dead
                UserMacLog.user_id=self.user.id
                UserMacLog.save()

            else:
                ## BAKİYE YOK
                raise forms.ValidationError("Bakiyeniz Yeterli Değil Lütfen Yükleme Yapın !")
        else:
            raise forms.ValidationError("Cihaz Mevcut Değil Kaldırılmış Olabilir !")


#########################################################################
# ÖDEME BİLDİRİMİ FORMU
class PaymentForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super(PaymentForm, self).__init__(*args,**kwargs)

    class Meta:
        model=Payment
        fields=[
            'fullname','bankname','iban','amount','cellphone'
        ]

    def clean(self):
        fullname=self.cleaned_data.get('fullname')
        bankname=self.cleaned_data.get('bankname')
        iban=self.cleaned_data.get('iban')
        amount=self.cleaned_data.get('amount')
        cellphone=self.cleaned_data.get('cellphone')

        if fullname and bankname and iban and amount and cellphone:
            if len(cellphone)>14:
                ## İstenilen Bilgiler Doğru Bildirimi Oluşturalım
                Pay=Payment()
                Pay.user_id=self.user.id
                Pay.fullname=fullname
                Pay.bankname=bankname
                Pay.iban=iban
                Pay.amount=amount
                Pay.cellphone=cellphone
                Pay.save()
                ## Kayıt Oluşturuldu
            else:
                ## Telefon Numarası Yanlış
                raise forms.ValidationError("Telefon Numarasını Doğru Giriniz")
        else:
            ## İSTENİLEN ALANLAR BOŞ
            raise forms.ValidationError("İstenilen Tüm Alanları Doldurun !")