from django.contrib import admin

from authentication.models import CustomUserAdmin, CustomUser

admin.site.register(CustomUser)
