# Generated by Django 2.0.3 on 2018-03-15 08:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_user_machine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_machine',
            name='machine',
            field=models.OneToOneField(on_delete=False, to='app.machine'),
        ),
        migrations.AlterField(
            model_name='user_machine',
            name='user',
            field=models.OneToOneField(on_delete=False, to=settings.AUTH_USER_MODEL),
        ),
    ]