# Generated by Django 5.1.6 on 2025-03-11 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artworks', '0004_artwork_rejection_reason_artwork_reviewed_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='sold',
            field=models.BooleanField(default=False),
        ),
    ]
