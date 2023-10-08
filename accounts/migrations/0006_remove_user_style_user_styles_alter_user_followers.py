# Generated by Django 4.2.5 on 2023-10-08 21:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_remove_article_style_article_styles_and_more'),
        ('accounts', '0005_alter_user_followers_alter_user_style'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='style',
        ),
        migrations.AddField(
            model_name='user',
            name='styles',
            field=models.ManyToManyField(blank=True, related_name='users', to='articles.style'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followees', to=settings.AUTH_USER_MODEL),
        ),
    ]