# Generated by Django 2.2.1 on 2019-06-06 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_auto_20190606_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.CharField(default=None, max_length=100)),
                ('user_id', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]
