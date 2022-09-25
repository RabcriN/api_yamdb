# Generated by Django 2.2.16 on 2022-09-24 18:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('titles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='titles.Title'),
        ),
        migrations.AddField(
            model_name='genre_title',
            name='genre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='titles.Genre'),
        ),
        migrations.AddField(
            model_name='genre_title',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='titles.Title'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='rewiew',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='titles.Review'),
        ),
        migrations.AddField(
            model_name='comment',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='titles.Title'),
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_review'),
        ),
    ]