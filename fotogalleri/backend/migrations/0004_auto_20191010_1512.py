# Generated by Django 2.2.5 on 2019-10-10 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20191007_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemetadata',
            name='event',
            field=models.CharField(default=2019, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='year',
            field=models.IntegerField(default=2018),
            preserve_default=False,
        ),
    ]
