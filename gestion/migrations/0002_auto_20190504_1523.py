# Generated by Django 2.0.8 on 2019-05-04 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='leasing',
            name='debit_authorization',
            field=models.BooleanField(default=False, verbose_name='Autorisation de prélèvement'),
        ),
        migrations.AddField(
            model_name='leasing',
            name='internal_rules_signed',
            field=models.BooleanField(default=False, verbose_name='Règlement intérieur signé'),
        ),
        migrations.AddField(
            model_name='leasing',
            name='photo',
            field=models.BooleanField(default=False, verbose_name="Photo d'identité"),
        ),
        migrations.AddField(
            model_name='leasing',
            name='school_certificate',
            field=models.BooleanField(default=False, verbose_name='Certificat de scolarité'),
        ),
        migrations.AlterField(
            model_name='leasing',
            name='guarantee',
            field=models.BooleanField(default=False, verbose_name='Engagement de caution'),
        ),
    ]