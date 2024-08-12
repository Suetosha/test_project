from django.contrib import admin

from django_app.models import Menu, Item


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class MenuItemAdmin(admin.ModelAdmin):
    pass

