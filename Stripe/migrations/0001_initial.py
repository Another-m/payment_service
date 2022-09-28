# Generated by Django 4.1.1 on 2022-09-28 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.IntegerField(default=0, verbose_name='Цена')),
                ('currency', models.CharField(choices=[('rub', 'РУБ'), ('usd', 'USD')], default='rub', max_length=3, verbose_name='Валюта')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='ItemOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, verbose_name='Количество')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='Stripe.item', verbose_name='Товар')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='Stripe.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Подкрепить к разделу',
                'verbose_name_plural': 'Подкрепить к разделу',
            },
        ),
        migrations.AddConstraint(
            model_name='itemorder',
            constraint=models.UniqueConstraint(fields=('item_id', 'order_id'), name='names'),
        ),
    ]