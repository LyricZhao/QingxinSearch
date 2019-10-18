# Generated by Django 2.2 on 2019-10-18 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('journal', models.TextField()),
                ('title', models.TextField()),
                ('content', models.TextField()),
                ('keys', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DictItem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('word', models.TextField()),
            ],
        ),
    ]