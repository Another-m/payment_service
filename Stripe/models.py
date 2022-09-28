from django.db import models



class Item(models.Model):
    CURRENCY = (
        ("rub", 'РУБ'),
        ("usd", 'USD'),
    )

    name = models.CharField(verbose_name='Наименование', max_length=50)
    description = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена', default=0)
    currency = models.CharField(verbose_name='Валюта', choices=CURRENCY, max_length=3, default="rub")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ItemOrder(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='items', verbose_name='Товар')
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order', verbose_name='Заказ')
    quantity = models.IntegerField(verbose_name='Количество', default=1)


    class Meta:
        verbose_name = 'Подкрепить к разделу'
        verbose_name_plural = 'Подкрепить к разделу'
        constraints = [
            models.UniqueConstraint(fields=['item_id', 'order_id'], name='names')
        ]

    def __str__(self):
        return str(self.item_id.name)
