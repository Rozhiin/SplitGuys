# Generated by Django 2.2.1 on 2019-06-06 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_cache_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cache',
            name='value',
            field=models.FloatField(default=0),
        ),
    ]
