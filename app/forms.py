from django import forms
from .models import User
from django.contrib.auth import authenticate

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
            'tel'
        ]