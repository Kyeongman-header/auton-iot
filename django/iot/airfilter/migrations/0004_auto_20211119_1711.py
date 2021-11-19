# Generated by Django 3.2.9 on 2021-11-19 17:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airfilter', '0003_auto_20211119_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airkorea',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 351621), verbose_name='airkor date published'),
        ),
        migrations.AlterField(
            model_name='gps',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 347853), null=True),
        ),
        migrations.AlterField(
            model_name='machine',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 347280)),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 348911)),
        ),
        migrations.AlterField(
            model_name='qr',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 348348)),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 351115), verbose_name='sensor date published'),
        ),
        migrations.AlterField(
            model_name='seven_days',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 352109), verbose_name='Seven days data published'),
        ),
        migrations.AlterField(
            model_name='thirty_days',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 17, 11, 6, 352669), verbose_name='Thirty days data published'),
        ),
    ]