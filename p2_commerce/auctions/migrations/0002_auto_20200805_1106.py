# Generated by Django 3.0.8 on 2020-08-05 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='latestBid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ltBid', to='auctions.Bid'),
        ),
    ]
