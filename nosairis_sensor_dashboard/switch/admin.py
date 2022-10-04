from atexit import register
import site
from django.contrib import admin
from .models import *

class SwitchAdmin(admin.ModelAdmin):
  model = Switch
  list_display= ['id','switch','status','timestamp']

admin.site.register(Switch, SwitchAdmin)
admin.site.register(SwitchArray)
