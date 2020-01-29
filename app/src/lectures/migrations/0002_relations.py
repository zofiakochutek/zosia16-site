# Generated by Django 2.2.8 on 2019-12-13 13:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conferences', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lectures', '0001_initial'),
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