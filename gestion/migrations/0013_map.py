# Generated by Django 2.0.5 on 2018-08-24 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0012_auto_20180715_1136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Map',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('map', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'Plan',
            },
        ),
    ]