# Generated by Django 3.2.9 on 2021-11-08 23:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0010_auto_20211109_0301'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]