# Generated by Django 3.2.3 on 2021-06-03 12:37

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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('book', models.FileField(blank=True, null=True, upload_to='books/', verbose_name='Документы')),
                ('image', models.ImageField(default='uploads/painbook.png', upload_to='uploads/')),
                ('bo', models.TextField(blank=True, max_length=1000, verbose_name='Библиографическое описание')),
                ('razdel', models.ManyToManyField(to='biblio.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='biblio.content')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
