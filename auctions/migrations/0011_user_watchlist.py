# Generated by Django 3.2.9 on 2021-11-09 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20211109_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watched_by', to='auctions.Auction'),
        ),
    ]
