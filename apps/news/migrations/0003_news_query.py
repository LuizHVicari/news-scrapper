# Generated by Django 5.1 on 2024-08-27 23:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_news_alter_query_query_term'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='query',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='news.query', verbose_name='busca'),
        ),
    ]
