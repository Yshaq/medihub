# Generated by Django 3.2.8 on 2021-11-04 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(default=12345, max_length=16),
        ),
    ]