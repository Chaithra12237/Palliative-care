# Generated by Django 4.0 on 2021-12-10 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='providers',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='users',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]