from django.contrib import admin
from .models import Hisse

@admin.register(Hisse)
class HisseAdmin(admin.ModelAdmin):
    list_display = ('sembol', 'isim')
    search_fields = ('sembol', 'isim')

# Alternatif olarak, admin.site.register(Hisse, HisseAdmin) yöntemini de kullanabilirsiniz.
