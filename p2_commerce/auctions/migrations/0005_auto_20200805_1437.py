# Generated by Django 3.0.8 on 2020-08-05 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20200805_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listings',
            field=models.ManyToManyField(blank=True, related_name='watch', to='auctions.Listing'),
        ),
    ]
