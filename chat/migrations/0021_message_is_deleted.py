# Generated by Django 3.1.5 on 2022-11-26 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0020_message_gift_message_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]