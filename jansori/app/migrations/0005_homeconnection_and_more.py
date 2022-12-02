# Generated by Django 4.1.3 on 2022-12-01 14:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_homeappliance_alter_recent_recent_clean_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeConnection',
            fields=[
                ('connect_id', models.OneToOneField(db_column='home_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.user')),
                ('air_conditioner', models.BooleanField(default=0)),
                ('air_purifier', models.BooleanField(default=0)),
                ('tv', models.BooleanField(default=0)),
                ('robot_clean', models.BooleanField(default=0)),
            ],
            options={
                'db_table': 'homeconnection',
            },
        ),
        migrations.RenameField(
            model_name='homeappliance',
            old_name='air_puritier_name',
            new_name='air_purifier_name',
        ),
        migrations.RemoveField(
            model_name='homeappliance',
            name='air_conditioner',
        ),
        migrations.RemoveField(
            model_name='homeappliance',
            name='air_puritier',
        ),
        migrations.RemoveField(
            model_name='homeappliance',
            name='robot_clean',
        ),
        migrations.RemoveField(
            model_name='homeappliance',
            name='tv',
        ),
        migrations.AlterField(
            model_name='recent',
            name='recent_clean',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 23, 13, 12, 702473)),
        ),
        migrations.AlterField(
            model_name='recent',
            name='recent_exercise',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 23, 13, 12, 702473)),
        ),
        migrations.AlterField(
            model_name='recent',
            name='recent_meal',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 1, 23, 13, 12, 702473)),
        ),
    ]
