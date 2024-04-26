# Generated by Django 4.2.4 on 2024-04-26 19:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0003_apimtnbundleprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mtnapiusers',
            name='user_id',
        ),
        migrations.AddField(
            model_name='mtnapiusers',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
