# Generated by Django 2.2.1 on 2019-05-13 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom du document')),
                ('english_name', models.CharField(blank=True, max_length=255, verbose_name='Nom du document (anglais)')),
                ('document', models.FileField(upload_to='', verbose_name='Fichier')),
                ('english_document', models.FileField(blank=True, null=True, upload_to='', verbose_name='Fichier (anglais)')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('english_description', models.TextField(blank=True, verbose_name='Description (anglais)')),
                ('active', models.BooleanField(default=True, verbose_name='Actif')),
            ],
        ),
    ]
