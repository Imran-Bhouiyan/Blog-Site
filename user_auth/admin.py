from django.contrib import admin
from .models import *
@admin.register(User)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = (
        'id',
        'username',
        'email',
        'is_active',
        'user_id',
    )
    list_filter = (
        'id',
        'username',
        'email',
        'is_active',
        'user_id',
    )


@admin.register(VerifyCode)
class PostAdmin(admin.ModelAdmin):
    '''Admin View for Post'''

    list_display = (
        'id',
        'code',
        'email',
       
    )
    list_filter = (
          'id',
        'code',
        'email',
    )
