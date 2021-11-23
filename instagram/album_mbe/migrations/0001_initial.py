# Generated by Django 3.2.9 on 2021-11-22 16:44

import album_mbe.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('draft', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('name', models.CharField(editable=False, max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserSimilarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('similarity_score', models.IntegerField()),
                ('similar_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='similar_user', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserFollows',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follows', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='followed_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=1000, upload_to=album_mbe.models.picture_directory_path)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='pictures', to='album_mbe.album')),
            ],
        ),
        migrations.CreateModel(
            name='Caption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=16)),
                ('x_pos', models.IntegerField()),
                ('y_pos', models.IntegerField()),
                ('size', models.IntegerField()),
                ('picture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='captions', to='album_mbe.picture')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='hash_tags',
            field=models.ManyToManyField(to='album_mbe.HashTag'),
        ),
        migrations.AddField(
            model_name='album',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
