from django.contrib import admin

from reviews.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio'
    )
    search_fields = ('role',)    
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
