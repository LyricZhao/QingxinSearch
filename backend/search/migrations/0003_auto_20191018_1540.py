# Generated by Django 2.2 on 2019-10-18 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_passwd'),
    ]

    operations = [
        migrations.AddField(
            model_name='dictitem',
            name='ids',
            field=models.ManyToManyField(to='search.Article'),
        ),
        migrations.AlterField(
            model_name='dictitem',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
