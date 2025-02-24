# Generated by Django 5.1.3 on 2025-02-24 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_hashtag_post_tags'),
        ('users', '0007_delete_mymountain'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='bookmark_posts',
        ),
        migrations.AddField(
            model_name='user',
            name='save_posts',
            field=models.ManyToManyField(blank=True, related_name='save_users', to='posts.post', verbose_name='저장한 Post 목록'),
        ),
    ]
