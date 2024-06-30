# Generated by Django 5.0.6 on 2024-06-26 12:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoitem',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='videoitem',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='released_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
