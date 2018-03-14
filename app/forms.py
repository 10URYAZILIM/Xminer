from django import forms
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

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


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'first_name',
            'last_name',
            'tel',
            'tc_no',
            'email'
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


class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            'avatar'
        ]
