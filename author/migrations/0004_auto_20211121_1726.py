# Generated by Django 3.2.8 on 2021-11-22 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_auto_20211028_0931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
