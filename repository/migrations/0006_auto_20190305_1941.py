# Generated by Django 2.1.4 on 2019-03-05 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20190305_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='theme',
            field=models.IntegerField(choices=[(1, 'warm'), (2, 'cold')], max_length=32, verbose_name='博客主题'),
        ),
    ]
