from django.db import models
from django.contrib.auth.models import AbstractUser

class Manager(AbstractUser):
    tg_id = models.BigIntegerField(null=True, blank=True)

class City(models.Model):
    title = models.CharField(blank=False, max_length=255)

    def __str__(self) -> str:
        return self.title

class Statement(models.Model):
    user = models.ForeignKey('app.Manager', null=True, blank=True, on_delete=models.SET_NULL)
    pickup = models.ForeignKey('app.City', null=True, blank=False, on_delete=models.PROTECT)
    dropoff = models.ForeignKey('app.City', null=True, blank=False, on_delete=models.PROTECT, related_name="dropoff_city")
    shipment_date = models.DateField(null=True, blank=False)
    end_date = models.DateField(null=True, blank=False)
    TRANSPORT_TYPE_CHOICES = [
        (1, 'Тент (Стандарт)'),
        (2, 'Тент ( Паровоз)'),
        (3, 'Рефрегиратор'),
    ]
    transport_type = models.IntegerField(null=True, blank=False, choices=TRANSPORT_TYPE_CHOICES)
    cargo = models.CharField(null=True, blank=False, max_length=255)
    load_capacity = models.IntegerField(null=True, blank=False) # kub
    weight = models.IntegerField(null=True, blank=False) # in tonn
    end = models.BooleanField(default=False)

    @property
    def direction(self):
        return f"{self.pickup} - {self.dropoff}"

class Request(models.Model):
    statement = models.ForeignKey('app.Statement', null=True, blank=True, on_delete=models.PROTECT)
    user = models.ForeignKey('app.Manager', null=True, blank=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(null=True, auto_now_add=True, db_index=True)
    price = models.BigIntegerField(null=True, blank=False)
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('sum', "So'm")
    ]
    currency = models.CharField(null=True, blank=False, max_length=8, choices=CURRENCY_CHOICES)
    comment = models.TextField(null=True, blank=True, max_length=1024)
    selected = models.BooleanField(default=False)
