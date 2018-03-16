# Generated by Django 2.0.3 on 2018-03-15 10:17

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20180315_1241'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_machine',
            name='machine_dead',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Makine Ölüm Zamanı'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user_machine',
            name='user',
            field=models.ForeignKey(on_delete=False, related_name='usermachine', to=settings.AUTH_USER_MODEL),
        ),
    ]
