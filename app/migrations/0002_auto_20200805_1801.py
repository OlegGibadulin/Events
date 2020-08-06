# Generated by Django 3.0.8 on 2020-08-05 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('surname', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Procedure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('ref_num', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.RenameField(
            model_name='event',
            old_name='start_time',
            new_name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='price',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='patient',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.PROTECT, to='app.Patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='procedures',
            field=models.ManyToManyField(blank=True, to='app.Procedure'),
        ),
    ]
