# Generated by Django 3.0.7 on 2020-06-30 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='restaurant',
            field=models.CharField(max_length=100),
        ),
    ]
