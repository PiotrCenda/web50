# Generated by Django 3.2.9 on 2021-11-03 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20211103_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='image_url',
            field=models.CharField(blank=True, default=None, max_length=300),
        ),
    ]
