from django.contrib import admin

# Register your models here.

from .models import BlogPost, AppUser, Comment,Like



admin.site.register(BlogPost)
admin.site.register(AppUser)
admin.site.register(Comment)
admin.site.register(Like)
