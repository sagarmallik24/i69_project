# Generated by Django 3.1.5 on 2022-11-19 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defaultPicker', '0005_auto_20221118_1316'),
    ]

    operations = [
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='ethnicity',
            name='ethnicity_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='family',
            name='familyPlans_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='gender',
            name='gender_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='politics',
            name='politics_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='religious',
            name='religious_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='searchgender',
            name='searchGender_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='tags',
            name='tag_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_am',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_az',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_be',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_bg',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_bn',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_bs',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_ca',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_et',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_eu',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_gl',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_hy',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_ka',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_km',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_la',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_lv',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_sq',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
        migrations.AddField(
            model_name='zodiacsign',
            name='zodiacSign_th',
            field=models.CharField(blank=True, max_length=265, null=True),
        ),
    ]