from django.contrib import admin
from .models import User,machine

class musteriler(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','tel','tc_no','hesap']
    list_display_links = ['username','first_name','last_name','email','tel','tc_no','hesap']
    search_fields = ['username','tel','tc_no']
    class Meta:
        model=User

class cihaz_ekle(admin.ModelAdmin):
    list_display = ['model','fiyat','miner_power']
    list_display_links = ['model','fiyat','miner_power']
    search_fields = ['model']
    class Meta:
        model=machine


admin.site.register(User,musteriler)
admin.site.register(machine,cihaz_ekle)
admin.site.site_header='Coinet Admin Paneli'
admin.site.site_title="Bitfindeks Mining"
