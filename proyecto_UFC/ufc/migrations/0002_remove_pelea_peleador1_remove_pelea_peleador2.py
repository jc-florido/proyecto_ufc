# Generated by Django 5.1.3 on 2025-01-22 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ufc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pelea',
            name='peleador1',
        ),
        migrations.RemoveField(
            model_name='pelea',
            name='peleador2',
        ),
    ]
