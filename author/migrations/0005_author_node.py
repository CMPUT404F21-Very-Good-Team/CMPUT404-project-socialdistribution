# Generated by Django 3.2.8 on 2021-11-23 17:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0005_auto_20211121_1736'),
        ('author', '0004_auto_20211121_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.node'),
        ),
    ]