from django.contrib import admin

# Register your models here.
from travel.models import Photo, Like, Comment

admin.site.register(Photo)
admin.site.register(Like)
admin.site.register(Comment)
