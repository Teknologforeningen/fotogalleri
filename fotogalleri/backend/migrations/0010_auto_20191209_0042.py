# Generated by Django 2.2.7 on 2019-12-08 22:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20191209_0029'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='imagepath',
            constraint=models.UniqueConstraint(condition=models.Q(parent=None), fields=('path',), name='unique_root_path'),
        ),
    ]
