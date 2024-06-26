# Generated by Django 4.2.4 on 2024-05-03 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intel_app', '0005_brand_category_order_product_productimage_orderitem_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category/'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='product_images/'),
        ),
    ]
