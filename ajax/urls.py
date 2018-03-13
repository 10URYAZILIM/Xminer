from django.urls import path,include
from .views import *
app_name="ajax"
urlpatterns = [
   path('login',login,name='login'),
   path('update_user',update_user,name='update_user'),
   path('update_password',update_password,name='update_password'),
   path('update_avatar',update_avatar,name='update_avatar')
]