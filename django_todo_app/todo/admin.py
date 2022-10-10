from django.contrib import admin
from .models import *

class TodoAdmin(admin.ModelAdmin):
  model = ToDo
  list_display= ['id','title','description','modified_at','created_at']

  fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title','description',),
        }),
        ('Logging Date',{
          'fields': ('modified_at','created_at',),
        }),
    )
  
  readonly_fields = [
        'modified_at',
        'created_at',
    ]

admin.site.register(ToDo, TodoAdmin)