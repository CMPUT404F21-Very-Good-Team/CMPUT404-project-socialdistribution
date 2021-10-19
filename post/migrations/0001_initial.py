# Generated by Django 3.2.8 on 2021-10-18 23:42

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('postID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('content', models.TextField()),
                ('isPublic', models.BooleanField()),
                ('isListed', models.BooleanField()),
                ('hasImage', models.BooleanField()),
                ('contentType', models.CharField(max_length=16)),
                ('host', models.URLField()),
                ('ownerID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('authorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('postID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('commentID', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('content', models.TextField()),
                ('contentType', models.CharField(max_length=16)),
                ('authorID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='author.author')),
                ('postID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
        migrations.AddConstraint(
            model_name='like',
            constraint=models.UniqueConstraint(fields=('postID', 'authorID'), name='Unique Like'),
        ),
    ]
