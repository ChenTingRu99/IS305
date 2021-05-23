# Generated by Django 3.2.3 on 2021-05-23 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('public_name', models.CharField(max_length=255)),
                ('wechat_id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('public_image', models.CharField(max_length=255)),
                ('authentication', models.CharField(blank=True, max_length=255, null=True)),
                ('introduction', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'accounts',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('account', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('url', models.CharField(max_length=2083)),
                ('images', models.CharField(max_length=255)),
                ('abstract', models.CharField(blank=True, max_length=255, null=True)),
                ('publish_date', models.CharField(max_length=255)),
            ],
            options={
                'db_table': '上海交通大学',
                'managed': False,
            },
        ),
    ]
