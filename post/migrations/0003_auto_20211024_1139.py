# Generated by Django 3.1.6 on 2021-10-24 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_like_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='post',
            name='origin',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='source',
            field=models.URLField(null=True),
        ),
    ]