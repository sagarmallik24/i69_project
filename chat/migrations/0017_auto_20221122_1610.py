# Generated by Django 3.1.5 on 2022-11-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20221121_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='data',
            field=models.CharField(max_length=50000, null=True),
        ),
    ]
