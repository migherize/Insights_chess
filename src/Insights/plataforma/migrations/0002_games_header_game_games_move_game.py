# Generated by Django 4.0.4 on 2022-05-24 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='games',
            name='header_game',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='games',
            name='move_game',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
