# Generated by Django 5.0.8 on 2024-09-25 04:59

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dating_profiles', '0002_rename_interestrequest_dating_interestrequest_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DatingProfileView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('viewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_viewed', to=settings.AUTH_USER_MODEL)),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_viewer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
