# Generated by Django 3.1.5 on 2022-10-18 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_moderatoronlinescheduler_list_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moderatoronlinescheduler',
            name='ofline_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='moderatoronlinescheduler',
            name='online_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]