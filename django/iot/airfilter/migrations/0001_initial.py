# Generated by Django 3.2.9 on 2021-11-24 16:20

import datetime
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 181002))),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('car_number', models.CharField(blank=True, max_length=20, null=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 179391))),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Thirty_Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thirty_days_sensor_avg', models.JSONField(blank=True, null=True)),
                ('thirty_days_sensor_max', models.JSONField(blank=True, null=True)),
                ('thirty_days_airkorea_avg', models.JSONField(blank=True, null=True)),
                ('thirty_days_airkorea_max', models.JSONField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 184650), verbose_name='Thirty days data published')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Seven_Days',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seven_days_sensor_avg', models.JSONField(blank=True, null=True)),
                ('seven_days_sensor_max', models.JSONField(blank=True, null=True)),
                ('seven_days_airkorea_avg', models.JSONField(blank=True, null=True)),
                ('seven_days_airkorea_max', models.JSONField(blank=True, null=True)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 184097), verbose_name='Seven days data published')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sensor', models.JSONField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 183046), verbose_name='sensor date published')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
        migrations.CreateModel(
            name='QR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('raw_id', models.CharField(blank=True, max_length=200, null=True)),
                ('qr', models.URLField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 180457))),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
        migrations.CreateModel(
            name='GPS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gps', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 179929), null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
        migrations.CreateModel(
            name='AirKorea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airkorea', models.JSONField()),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2021, 11, 24, 16, 20, 10, 183564), verbose_name='airkor date published')),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='airfilter.machine')),
            ],
        ),
    ]
