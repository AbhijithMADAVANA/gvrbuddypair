# Generated by Django 5.0.8 on 2024-09-30 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('U_auth', '0005_userpreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='costume_user',
            name='is_subscribed',
            field=models.BooleanField(default=False),
        ),
    ]
