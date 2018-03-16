from django.contrib import admin
from .models import User

class musteriler(admin.ModelAdmin):
    list_display = ['username','first_name','last_name','email','tel','tc_no','hesap']
    list_display_links = ['username','first_name','last_name','email','tel','tc_no','hesap']
    search_fields = ['username','tel','tc_no']
    class Meta:
        model=User



admin.site.register(User,musteriler)
admin.site.site_header='Coinet Admin Paneli'
admin.site.site_title="Bitfindeks Mining"
from .models import machine



admin.site.register(machine)
