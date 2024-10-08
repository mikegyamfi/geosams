# Generated by Django 4.2.4 on 2024-08-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0020_mtntransaction_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfitInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selling_price_total', models.FloatField()),
                ('purchase_price_total', models.FloatField(blank=True, null=True)),
                ('profit', models.FloatField()),
                ('date_and_time', models.DateTimeField(auto_now_add=True)),
                ('channel', models.CharField(max_length=250)),
            ],
        ),
        migrations.AlterField(
            model_name='mtntransaction',
            name='transaction_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('Canceled', 'Canceled')], default='Pending', max_length=100),
        ),
    ]
