# Generated by Django 3.2.8 on 2021-11-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airfilter', '0002_auto_20211103_0359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machine',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
