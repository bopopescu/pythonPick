# Generated by Django 2.2.6 on 2019-12-17 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_picture_authorusername'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='authorUsername',
            field=models.CharField(default='defaultUsername', max_length=255),
            preserve_default=False,
        ),
    ]
