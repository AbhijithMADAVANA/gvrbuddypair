# Generated by Django 5.0.8 on 2024-09-24 11:03

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferred_gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('B', 'Both')], max_length=1)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_preferred_gender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
