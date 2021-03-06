# Generated by Django 2.2 on 2019-10-31 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('journal', models.TextField()),
                ('title', models.TextField()),
                ('text', models.TextField()),
                ('content', models.TextField()),
                ('keys', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Passwd',
            fields=[
                ('id', models.TextField(primary_key=True, serialize=False)),
                ('passwd', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='DictItem',
            fields=[
                ('word', models.TextField(primary_key=True, serialize=False)),
                ('ids', models.ManyToManyField(to='search.Article')),
            ],
        ),
    ]
