from django.contrib import admin
from .models import Category, Photo


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


# Register your models here.
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
