# Generated by Django 2.2.4 on 2019-09-18 16:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('conferences', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userpreferences',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.Organization'),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='userpreferences',
            name='zosia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='conferences.Zosia'),
        ),
        migrations.AddField(
            model_name='bus',
            name='zosia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buses', to='conferences.Zosia'),
        ),
    ]
