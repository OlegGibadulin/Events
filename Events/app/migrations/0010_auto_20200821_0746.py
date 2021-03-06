# Generated by Django 3.0.8 on 2020-08-21 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20200821_0741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='procedure',
            name='user',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='app.UserProfile'),
        ),
    ]
