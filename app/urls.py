from django.urls import path,include
from .views import *

app_name="app"

urlpatterns = [
    path('',index,name='index'),
    path('user',user,name='user'),
    path('market',market,name='market'),
    path('store',store,name='store'),
    path('logout',user_logout,name='logout'),

]
