# Generated by Django 3.2.8 on 2021-11-22 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20211121_1726'),
    ]

    operations = [
        migrations.RenameField(
            model_name='node',
            old_name='authentication',
            new_name='password',
        ),
        migrations.AddField(
            model_name='node',
            name='username',
            field=models.TextField(default='test'),
            preserve_default=False,
        ),
    ]
