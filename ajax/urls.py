from django.urls import path,include
from .views import *
app_name="ajax"
urlpatterns = [
   path('login',login,name='login')
]