# Generated by Django 2.2.6 on 2019-10-29 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lectures', '0003_alter_field_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lecture',
            name='info',
        ),
        migrations.AddField(
            model_name='lecture',
            name='events',
            field=models.CharField(blank=True, help_text="Are you planning any event after your lecture or workshop (e.g. pizza, drinks, games, recruitment)? Beware that organizers WON'T ALLOW you to arrange your event if you don't announce it here!", max_length=800, null=True, verbose_name='Additional events'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='requests',
            field=models.CharField(blank=True, help_text='Your requests, suggestions or comments intended for organizers', max_length=800, null=True, verbose_name='Requests or comments'),
        ),
    ]
