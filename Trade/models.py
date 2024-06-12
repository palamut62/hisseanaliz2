from django.db import models

# models.py
from django.db import models

class Hisse(models.Model):
    sembol = models.CharField(max_length=10, blank=True)
    isim = models.CharField(max_length=100, blank=True)
    lot_adedi = models.IntegerField(default=1)  # Varsayılan değer olarak 1

    def __str__(self):
        return self.sembol



class UygulamaAyarları(models.Model):
    api_key = models.CharField(max_length=255, blank=True, null=True)
    ayar_adi = models.CharField(max_length=100, unique=True)
    ayar_degeri = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ayar_adi


from django.db import models

class Settings(models.Model):
    key = models.CharField(max_length=50, unique=True,blank=None)
    value = models.CharField(max_length=500,blank=True, null=True)

    def __str__(self):
        return self.key



