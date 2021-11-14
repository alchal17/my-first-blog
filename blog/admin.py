from django.contrib import admin
from .models import *


class AdminPost(admin.ModelAdmin):
    list_display = ('title', 'author', 'text',)


class AdminCategory(admin.ModelAdmin):
    list_display = ('category_title', )


class AdminTag(admin.ModelAdmin):
    list_display = ('tag_title', )


admin.site.register(Tag, AdminTag)
admin.site.register(Post, AdminPost)
admin.site.register(Category, AdminCategory)

