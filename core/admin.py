from django.contrib import admin

from . models import *

@admin.register(Connections)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = (
        'id',
      
       
    )
    list_filter = (
          'id',
       
    )
