# Generated by Django 3.2.8 on 2021-12-06 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_author_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='displayName',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='summary',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
