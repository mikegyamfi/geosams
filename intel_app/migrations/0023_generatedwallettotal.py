# Generated by Django 4.2.4 on 2024-10-04 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0022_alter_profitinstance_profit'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneratedWalletTotal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('date_generated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
