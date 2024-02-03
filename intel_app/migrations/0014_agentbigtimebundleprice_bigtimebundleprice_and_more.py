# Generated by Django 4.2.4 on 2024-01-19 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0013_topuprequestt'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentBigTimeBundlePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('bundle_volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='BigTimeBundlePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('bundle_volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SuperAgentBigTimeBundlePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('bundle_volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SuperAgentIshareBundlePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('bundle_volume', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='SuperAgentMTNBundlePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('bundle_volume', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='admininfo',
            name='afa_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='status',
            field=models.CharField(choices=[('User', 'User'), ('Agent', 'Agent'), ('Super Agent', 'Super Agent')], default='User', max_length=250),
        ),
        migrations.CreateModel(
            name='BigTimeTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_number', models.BigIntegerField()),
                ('offer', models.CharField(max_length=250)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('transaction_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=100)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AFARegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.BigIntegerField()),
                ('gh_card_number', models.CharField(max_length=256)),
                ('name', models.CharField(max_length=250)),
                ('occupation', models.CharField(blank=True, max_length=20)),
                ('reference', models.CharField(blank=True, max_length=20)),
                ('date_of_birth', models.DateField()),
                ('transaction_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=100)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
