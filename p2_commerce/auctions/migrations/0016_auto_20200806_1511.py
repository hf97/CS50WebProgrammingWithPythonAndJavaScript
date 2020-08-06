# Generated by Django 3.0.8 on 2020-08-06 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20200806_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wonlisting',
            name='listings',
        ),
        migrations.AddField(
            model_name='wonlisting',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auctions.Listing'),
        ),
    ]
