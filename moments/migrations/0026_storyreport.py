# Generated by Django 3.1.5 on 2022-10-29 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('moments', '0025_report_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Report_msg', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('story', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_for_report', to='moments.story')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_for_story_report', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
