# Generated by Django 5.0.8 on 2024-10-02 09:35

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matrimony_profiles', '0002_matrimonyfriendship'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatrimonyProfileViewCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('viewed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrimony_viewed_profiles', to=settings.AUTH_USER_MODEL)),
                ('viewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matrimony_profile_views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
