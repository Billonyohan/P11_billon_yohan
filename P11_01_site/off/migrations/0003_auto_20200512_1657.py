# Generated by Django 3.0.5 on 2020-05-12 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('off', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='message',
            field=models.TextField(max_length=1000),
        ),
    ]
