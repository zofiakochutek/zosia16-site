# Generated by Django 2.2.4 on 2019-09-18 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lectures', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('conferences', '0002_relations'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='zosia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conferences.Zosia', verbose_name='Conference'),
        ),
    ]
