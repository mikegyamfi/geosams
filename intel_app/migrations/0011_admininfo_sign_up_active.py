# Generated by Django 4.2.4 on 2024-05-10 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0010_alter_category_image_alter_productimage_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='admininfo',
            name='sign_up_active',
            field=models.BooleanField(default=False),
        ),
    ]
