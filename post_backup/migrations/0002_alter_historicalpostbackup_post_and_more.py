# Generated by Django 4.0.2 on 2022-02-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_backup', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpostbackup',
            name='post',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='postbackup',
            name='post',
            field=models.JSONField(default=dict),
        ),
    ]