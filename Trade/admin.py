from django.contrib import admin
from .models import Hisse, UygulamaAyarları,Settings


@admin.register(Hisse)
class HisseAdmin(admin.ModelAdmin):
    list_display = ('sembol', 'isim')
    search_fields = ('sembol', 'isim')

# Alternatif olarak, admin.site.register(Hisse, HisseAdmin) yöntemini de kullanabilirsiniz.

@admin.register(UygulamaAyarları)
class UygulamaAyarlarıAdmin(admin.ModelAdmin):
    list_display = ('ayar_adi', 'ayar_degeri')

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


