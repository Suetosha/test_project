from django.contrib import admin

from django_app.models import Menu, Item


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class MenuItemAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["parent"].required = False
        return form
