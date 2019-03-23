# Generated by Django 2.1.4 on 2019-03-05 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20190305_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleMoreInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.Article')),
            ],
            options={
                'verbose_name_plural': '文章内容',
            },
        ),
    ]
