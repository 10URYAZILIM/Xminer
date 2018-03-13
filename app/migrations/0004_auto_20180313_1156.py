# Generated by Django 2.0.3 on 2018-03-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user_tc_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tc_no',
            field=models.CharField(default=0, max_length=11, verbose_name='T.C Kimlik Numarası'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tel',
            field=models.CharField(default=0, max_length=20, verbose_name='Cep Telefonu'),
        ),
    ]
