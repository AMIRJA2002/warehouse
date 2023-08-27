# Generated by Django 4.2.4 on 2023-08-22 17:05

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('is_enable', models.BooleanField(default=True)),
                ('mac_address', models.CharField(max_length=17, unique=True)),
                ('end_rent_charge', models.DateTimeField(db_index=True, default=datetime.datetime.now)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='store.section')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
