# Generated by Django 2.0.8 on 2019-04-26 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0014_auto_20180824_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rent',
            name='rent2',
        ),
    ]