# ipo_backend/ipo_app/models.py

from django.db import models

class IPO(models.Model):
    slNumber = models.IntegerField()
    logo = models.ImageField(upload_to='ipo_logos/')  # Adjust this based on your needs
    name = models.CharField(max_length=255)
    symbol = models.CharField(max_length=10)
    priceBand = models.CharField(max_length=20)
    industry = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    closeDate = models.DateField()
    type = models.CharField(max_length=20)
    totalMarketCap = models.CharField(max_length=20)
    subscriptionNumber = models.CharField(max_length=10)
