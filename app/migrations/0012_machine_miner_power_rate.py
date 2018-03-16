# Generated by Django 2.0.3 on 2018-03-16 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='miner_power_rate',
            field=models.CharField(choices=[('TH', 'TH/s'), ('MH', 'MH/s'), ('GH', 'GH/s')], default='TH', max_length=10, verbose_name='Kazım Güç Türü'),
            preserve_default=False,
        ),
    ]
