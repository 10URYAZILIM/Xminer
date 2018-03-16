# Generated by Django 2.0.3 on 2018-03-16 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_machine_warranty'),
    ]

    operations = [
        migrations.AddField(
            model_name='machine',
            name='lifetime',
            field=models.CharField(choices=[('1 YIL', '1 YIL'), ('2 YIL', '2 YIL')], default='1 YIL', max_length=25, verbose_name='Kullanım Ömrü'),
            preserve_default=False,
        ),
    ]