# Generated by Django 2.0.3 on 2018-03-18 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20180318_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_machine_log',
            name='machine_id',
            field=models.IntegerField(default=1, verbose_name='MakinaID'),
            preserve_default=False,
        ),
    ]
