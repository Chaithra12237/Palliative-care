# Generated by Django 4.0 on 2021-12-11 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_service_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='organization',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
