# Generated by Django 3.1.5 on 2022-10-17 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('defaultPicker', '0002_language'),
        ('user', '0019_auto_20221017_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='language',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='defaultPicker.language', verbose_name='Language'),
        ),
    ]