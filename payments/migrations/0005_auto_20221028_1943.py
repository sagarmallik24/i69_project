# Generated by Django 3.1.5 on 2022-10-28 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_privatekey_publickey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bokupayment',
            name='charging_token',
            field=models.CharField(blank=True, max_length=65),
        ),
    ]
