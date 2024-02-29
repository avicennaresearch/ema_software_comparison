# Generated by Django 5.0.2 on 2024-03-21 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comparison', '0009_url_similar_urls'),
    ]

    operations = [
        migrations.AddField(
            model_name='software',
            name='is_monitored',
            field=models.BooleanField(default=True, verbose_name='Is Monitored'),
        ),
        migrations.AddField(
            model_name='software',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
    ]