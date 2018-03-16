from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar=models.ImageField(default=None,verbose_name="Profil Fotoğrafı",upload_to="users")
    hesap=models.FloatField(default=0,verbose_name="Hesap")
    tel=models.CharField(max_length=20,verbose_name="Cep Telefonu",default="(000) 000 00 00")
    tc_no=models.CharField(max_length=11,verbose_name="T.C Kimlik Numarası",default="00000000000")


class machine(models.Model):
    image=models.ImageField(verbose_name="Görsel",upload_to="machine")
    model=models.CharField(verbose_name="Model",max_length=50)
    properties=models.TextField(verbose_name="Özellikler")
    fiyat=models.FloatField(verbose_name="Fiyat")
    miner_power=models.FloatField(verbose_name="Kazım Gücü")

    def __str__(self):
        return self.model


class user_machine(models.Model):
    user=models.ForeignKey(User,on_delete=False,related_name="usermachine")
    machine=models.ForeignKey(machine,on_delete=False)
    date=models.DateTimeField(auto_now_add=True, verbose_name="Makina Alım Zamanı")
    machine_dead=models.DateTimeField(verbose_name="Makine Ölüm Zamanı")
    miner_power=models.FloatField(verbose_name="Kazım Gücü")
    fiyat=models.FloatField(verbose_name="Fiyat")

class news(models.Model):
    post=models.CharField(verbose_name="Kısa Yazı",max_length=400)
    title=models.CharField(verbose_name="Başlık",max_length=200)
    date=models.DateTimeField(auto_now_add=True,verbose_name="Zaman")

