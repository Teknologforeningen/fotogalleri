# Generated by Django 2.2.5 on 2019-10-11 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_auto_20191010_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagemetadata',
            name='event',
        ),
        migrations.RemoveField(
            model_name='imagemetadata',
            name='year',
        ),
        migrations.CreateModel(
            name='ImagePath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(editable=False, max_length=256, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ImagePath')),
            ],
        ),
        migrations.AddField(
            model_name='imagemetadata',
            name='path',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.ImagePath'),
        ),
    ]
