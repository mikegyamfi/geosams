# Generated by Django 4.2.4 on 2024-05-04 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0008_rename_wallettransactions_wallettransaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettransaction',
            name='new_balance',
            field=models.FloatField(null=True),
        ),
    ]
