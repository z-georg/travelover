from django.contrib import admin

# Register your models here.
from accounts.models import UserProfileInfo

admin.site.register(UserProfileInfo)