# Generated by Django 4.0.4 on 2022-08-01 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0003_alter_opening_n_eco_b_alter_opening_n_eco_db_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opening',
            name='n_eco_b',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='n_eco_db',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='n_eco_dw',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='n_eco_lb',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='n_eco_lw',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='opening',
            name='n_eco_ww',
            field=models.CharField(blank=True, default=None, max_length=200, null=True),
        ),
    ]
