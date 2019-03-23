# Generated by Django 2.1.4 on 2019-01-15 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trouble',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('detail', models.TextField()),
                ('ctime', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(1, '未处理'), (2, '处理中'), (3, '已处理')], default=1)),
                ('solution', models.TextField(null=True)),
                ('ptime', models.DateTimeField(null=True)),
                ('evaluate', models.IntegerField(choices=[(1, '不满意'), (2, '一般'), (3, '满意')], default=2, null=True)),
                ('processer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='p', to='repository.UserInfo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='u', to='repository.UserInfo')),
            ],
            options={
                'verbose_name_plural': '报障单',
            },
        ),
    ]
