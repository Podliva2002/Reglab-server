# Generated by Django 5.0.4 on 2024-05-03 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsender',
            name='curse_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
