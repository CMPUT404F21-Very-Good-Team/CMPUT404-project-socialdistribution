# Generated by Django 3.1.6 on 2021-10-12 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0001_initial'),
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inbox',
            name='postID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.post'),
        ),
        migrations.AddField(
            model_name='follow',
            name='fromAuthor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_following', to='author.author'),
        ),
        migrations.AddField(
            model_name='follow',
            name='toAuthor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_being_followed', to='author.author'),
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('fromAuthor', 'toAuthor'), name='Unique Follows'),
        ),
    ]
