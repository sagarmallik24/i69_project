# Generated by Django 3.1.5 on 2022-10-27 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bokupayment',
            name='billing_identity',
            field=models.CharField(blank=True, max_length=25),
        ),
    ]
