# Generated by Django 2.0.3 on 2018-03-15 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20180315_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_machine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Makina Alım Zamanı')),
                ('miner_power', models.FloatField(verbose_name='Kazım Gücü')),
                ('fiyat', models.FloatField(verbose_name='Fiyat')),
                ('machine', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.machine')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]