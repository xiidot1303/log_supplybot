from django.db import models
from django.contrib.auth.models import AbstractUser

class Manager(AbstractUser):
    tg_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name

class City(models.Model):
    title = models.CharField(verbose_name='Название города', blank=False, max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'

class Statement(models.Model):
    user = models.ForeignKey('app.Manager', verbose_name='Менеджер', null=True, blank=True, on_delete=models.SET_NULL)
    pickup = models.ForeignKey('app.City', verbose_name='Место отправки', null=True, blank=False, on_delete=models.PROTECT)
    dropoff = models.ForeignKey('app.City', verbose_name='Место доставки', null=True, blank=False, on_delete=models.PROTECT, related_name="dropoff_city")
    shipment_date = models.DateField(verbose_name='Дата отправки', null=True, blank=False)
    end_date = models.DateField(verbose_name='Дата завершения выписки', null=True, blank=False)
    TRANSPORT_TYPE_CHOICES = [
        (1, 'Тент (Стандарт)'),
        (2, 'Тент (Паровоз)'),
        (3, 'Рефрижератор'),
    ]
    transport_type = models.IntegerField(verbose_name='Тип транспорта', null=True, blank=False, choices=TRANSPORT_TYPE_CHOICES)
    cargo = models.CharField(verbose_name='Груз', null=True, blank=False, max_length=255)
    load_capacity = models.IntegerField(verbose_name='Грузоподъемность (куб)', null=True, blank=False)
    weight = models.IntegerField(verbose_name='Вес (тонн)', null=True, blank=False)
    end = models.BooleanField(verbose_name='Завершено', default=False)

    @property
    def direction(self):
        return f"{self.pickup} - {self.dropoff}"

    class Meta:
        verbose_name = 'Заявление'
        verbose_name_plural = 'Заявления'

class Request(models.Model):
    statement = models.ForeignKey('app.Statement', verbose_name='Заявление', null=True, blank=True, on_delete=models.PROTECT)
    user = models.ForeignKey('app.Manager', verbose_name='Менеджер', null=True, blank=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField(verbose_name='Дата и время', null=True, auto_now_add=True, db_index=True)
    price = models.BigIntegerField(verbose_name='Цена', null=True, blank=False)
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('sum', "Сум")
    ]
    currency = models.CharField(verbose_name='Валюта', null=True, blank=False, max_length=8, choices=CURRENCY_CHOICES)
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True, max_length=1024)
    selected = models.BooleanField(verbose_name='Выбрано', default=False)

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
