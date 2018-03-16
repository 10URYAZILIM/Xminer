# Generated by Django 2.0.3 on 2018-03-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20180316_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='warranty',
            field=models.CharField(choices=[('3 AY', '3 AY'), ('6 AY', '6 AY'), ('9 AY', '9 AY'), ('12 AY', '12 AY'), ('18 AY', '18 AY'), ('24 AY', '24 AY')], default='6 AY', max_length=25, verbose_name='Garanti Süresi'),
            preserve_default=False,
        ),
    ]
