# Generated by Django 5.1.3 on 2025-02-27 02:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mountains', '0002_mountain_detail_info_mountain_leadtime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mountain',
            name='leadtime',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
