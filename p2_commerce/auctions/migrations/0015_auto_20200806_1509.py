# Generated by Django 3.0.8 on 2020-08-06 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_wonlisting_didwarning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wonlisting',
            name='didWarning',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
