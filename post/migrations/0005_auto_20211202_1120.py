# Generated by Django 3.2.8 on 2021-12-02 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(null=True),
        ),
    ]