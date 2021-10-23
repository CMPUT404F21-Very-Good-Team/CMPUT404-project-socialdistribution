# Generated by Django 3.1.6 on 2021-10-22 22:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('authorID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('displayName', models.CharField(max_length=32)),
                ('host', models.URLField()),
                ('github', models.URLField(blank=True, null=True)),
                ('profileImage', models.URLField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inboxType', models.CharField(max_length=8)),
                ('summary', models.CharField(blank=True, max_length=40, null=True)),
                ('date', models.DateTimeField()),
                ('objectID', models.CharField(blank=True, max_length=200, null=True)),
                ('authorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inbox_owner', to='author.author')),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('fromAuthor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sender', to='author.author')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('fromAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_following', to='author.author')),
                ('toAuthor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_being_followed', to='author.author')),
            ],
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('fromAuthor', 'toAuthor'), name='Unique Follows'),
        ),
    ]
