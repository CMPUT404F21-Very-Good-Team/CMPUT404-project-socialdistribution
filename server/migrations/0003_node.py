# Generated by Django 3.1.6 on 2021-11-15 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_setting_allow_user_sign_up'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_url', models.URLField()),
                ('authentication', models.TextField()),
            ],
        ),
    ]