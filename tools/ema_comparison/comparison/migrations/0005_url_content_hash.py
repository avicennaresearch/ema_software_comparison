# Generated by Django 5.0.2 on 2024-03-19 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparison', '0004_rename_software_name_software_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='url',
            name='content_hash',
            field=models.CharField(default='NONE', max_length=128, verbose_name='Content Hash'),
            preserve_default=False,
        ),
    ]