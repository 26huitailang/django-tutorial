# Generated by Django 2.0.5 on 2018-06-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mzitu', '0002_downloadedsuit'),
    ]

    operations = [
        migrations.AddField(
            model_name='downloadedsuit',
            name='tag',
            field=models.CharField(default='', max_length=100),
        ),
    ]
