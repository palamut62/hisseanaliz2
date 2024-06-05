from django.db import models

class Hisse(models.Model):
    sembol = models.CharField(max_length=10, blank=True)
    isim = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.sembol
