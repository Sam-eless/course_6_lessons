# Generated by Django 4.2 on 2023-05-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=150, verbose_name='заголовок')),
                ('content', models.CharField(blank=True, max_length=150, null=True, verbose_name='содержимое')),
                ('slug', models.CharField(blank=True, max_length=255, unique=True, verbose_name='j_j')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='blog_entry/', verbose_name='изображение')),
                ('date_of_creation', models.DateTimeField(blank=True, null=True, verbose_name='дата создания')),
                ('is_published', models.BooleanField(verbose_name='опубликована ли статья?')),
                ('number_of_views', models.IntegerField(verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'пост',
                'verbose_name_plural': 'посты',
                'ordering': ('header',),
            },
        ),
    ]
