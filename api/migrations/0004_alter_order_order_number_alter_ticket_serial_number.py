# Generated by Django 4.0 on 2021-12-21 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_order_tickettype_remove_event_premium_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='serial_number',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
