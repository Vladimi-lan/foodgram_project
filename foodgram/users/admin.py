from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')
    list_filter = ('id',)


admin.site.register(CustomUser, CustomUserAdmin)