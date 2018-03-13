from django.urls import path,include
from .views import *

app_name="app"

urlpatterns = [
    path('',index,name='index'),
    path('user',user,name='user'),
    path('logout',index,name='logout'),

]
