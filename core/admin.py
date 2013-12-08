from django.contrib import admin
from core.models import UserExtension
# Register your models here.

class UserExtensionAdmin(admin.ModelAdmin):
	list_display = ['id', 'user', 'points', 'card', 'modified', 'created']

admin.site.register(UserExtension, UserExtensionAdmin)