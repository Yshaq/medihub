# Generated by Django 3.2.8 on 2021-11-05 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_merge_20211105_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(default=12345, max_length=16),
        ),
    ]
