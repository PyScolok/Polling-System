# Generated by Django 3.1.5 on 2021-01-21 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]