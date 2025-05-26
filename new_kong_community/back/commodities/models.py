from django.db import models
from django.conf import settings
# from articles.models import Article

# Create your models here.
class CommodityPrice(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=20)  # 예: 'GC=F'
    price = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)