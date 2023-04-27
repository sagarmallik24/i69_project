# Generated by Django 3.1.5 on 2022-11-18 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0031_userlimit'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModeratorQScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskName', models.CharField(choices=[('moderator_logout_intervel', 'moderator_logout_intervel'), ('unassign_moderator_from_inactive_to_active_worker_intervel', 'unassign_moderator_from_inactive_to_active_worker_intervel')], max_length=100)),
                ('numberOfPeriods', models.IntegerField(default=0)),
                ('intervalPeriod', models.CharField(choices=[('Days', 'Days'), ('Hours', 'Hours'), ('Minutes', 'Minutes'), ('Seconds', 'Seconds')], max_length=100)),
            ],
        ),
    ]
