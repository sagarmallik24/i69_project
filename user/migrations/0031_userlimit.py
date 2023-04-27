# Generated by Django 3.1.5 on 2022-11-18 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_auto_20221031_1603'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_name', models.CharField(choices=[('Stories', 'Stories'), ('Moments', 'Moments')], max_length=95, unique=True)),
                ('limit_value', models.PositiveIntegerField(default=2)),
            ],
        ),
    ]
