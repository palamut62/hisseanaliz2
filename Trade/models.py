from django.db import models

# models.py
from django.db import models

class Hisse(models.Model):
    sembol = models.CharField(max_length=10, blank=True)
    isim = models.CharField(max_length=100, blank=True)
    lot_adedi = models.IntegerField(default=1)  # Varsayılan değer olarak 1

    def __str__(self):
        return self.sembol

