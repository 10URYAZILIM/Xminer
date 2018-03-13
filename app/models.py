from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar=models.ImageField(default=None,verbose_name="Profil Fotoğrafı")
    hesap=models.FloatField(default=0,verbose_name="Hesap")
    tel=models.CharField(max_length=20,verbose_name="Cep Telefonu",default="(000) 000 00 00")
    tc_no=models.CharField(max_length=11,verbose_name="T.C Kimlik Numarası",default="00000000000")


