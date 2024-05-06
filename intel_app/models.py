import os
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

from intel_app.custom_storages import MediaStorage


# Create your models here.


# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False, unique=True)
    email = models.EmailField(max_length=250, null=False, blank=False)
    phone = models.PositiveIntegerField(null=True, blank=True)
    wallet = models.FloatField(null=True, blank=True, default=0.0)
    choices = (
        ("User", "User"),
        ("Agent", "Agent"),
        ("Super Agent", "Super Agent")
    )
    status = models.CharField(max_length=250, null=False, blank=False, choices=choices, default="User")
    password1 = models.CharField(max_length=100, null=False, blank=False)
    password2 = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.username


class AdminInfo(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    momo_numberr = models.PositiveBigIntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    choices = (
        ("MTN Mobile Money", "MTN Mobile Money"),
        ("Vodafone Cash", "Vodafone Cash"),
        ("AT Money", "AT Money")
    )
    payment_channell = models.CharField(max_length=250, choices=choices)
    afa_price = models.FloatField(null=True, blank=True)


class IShareBundleTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bundle_number = models.BigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_status = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"
    

class IshareBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class AgentIshareBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class SuperAgentIshareBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"
    

class MTNTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bundle_number = models.BigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    choices = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
    )
    transaction_status = models.CharField(max_length=100, choices=choices, default="Pending")
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class BigTimeBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class AgentBigTimeBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class SuperAgentBigTimeBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class MTNBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)


    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class AgentMTNBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)


    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class SuperAgentMTNBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)


    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class BigTimeTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bundle_number = models.BigIntegerField(null=False, blank=False)
    offer = models.CharField(max_length=250, null=False, blank=False)
    reference = models.CharField(max_length=20, null=False, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)
    choices = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
    )
    transaction_status = models.CharField(max_length=100, choices=choices, default="Pending")
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.bundle_number} - {self.reference}"


class AFARegistration(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone_number = models.BigIntegerField(null=False, blank=False)
    gh_card_number = models.CharField(null=False, blank=False, max_length=256)
    name = models.CharField(max_length=250, null=False, blank=False)
    occupation = models.CharField(max_length=20, null=False, blank=True)
    reference = models.CharField(max_length=20, null=False, blank=True)
    date_of_birth = models.DateField(null=False, blank=False)
    choices = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
        ("Failed", "Failed")
    )
    transaction_status = models.CharField(max_length=100, choices=choices, default="Pending")
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.phone_number} - {self.gh_card_number}"
    

class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reference = models.CharField(max_length=256, null=False, blank=False)
    amount = models.FloatField(null=True, blank=True)
    channels = (
        ("mtn", "mtn"),
        ("ishare", "ishare"),
        ("bigtime", "bigtime"),
        ("afa", "afa"),
        ("topup", "topup")
    )
    transaction_details = models.JSONField(null=True, blank=True)
    channel = models.CharField(max_length=250, null=True, blank=True, choices=channels)
    payment_description = models.CharField(max_length=500, null=True, blank=True)
    transaction_status = models.CharField(max_length=256, null=True, blank=True, default="Unfinished")
    transaction_date = models.CharField(max_length=250, null=True, blank=True)
    payment_details = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.reference}"


# class TopUpRequest(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     reference = models.CharField(max_length=250, null=False, blank=False)
#     amount = models.FloatField(blank=False, null=False)
#     status = models.BooleanField(default=False, blank=False, null=False)
#     date = models.DateTimeField(auto_now_add=True)
#     credited_at = models.DateTimeField(auto_now_add=True)


class TopUpRequestt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    reference = models.CharField(max_length=250, null=False, blank=False)
    amount = models.FloatField(blank=False, null=False)
    status = models.BooleanField(default=False, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)
    credited_at = models.DateTimeField(auto_now_add=True)


class APIMTNBundlePrice(models.Model):
    price = models.FloatField(null=False, blank=False)
    bundle_volume = models.FloatField(null=False, blank=False)

    def __str__(self):
        if self.bundle_volume >= 1000:
            return f"GHS{self.price} - {self.bundle_volume/1000}GB"
        return f"GHS{self.price} - {self.bundle_volume}MB"


class MTNAPIUsers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    wallet_balance = models.FloatField(null=False, blank=False)
    key = models.CharField(max_length=150, null=False, blank=False)


class APIUsersHistory(models.Model):
    mtn_transaction = models.ForeignKey(MTNTransaction, on_delete=models.CASCADE)
    api_user = models.ForeignKey(MTNAPIUsers, on_delete=models.CASCADE)


class ApiWalletTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choices = (
        ("Debit", "Debit"),
        ("Credit", "Credit"),
    )
    transaction_type = models.CharField(max_length=250, null=True, blank=True, choices=choices)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.FloatField(null=False)
    new_balance = models.FloatField(null=True)


####################################################################################

def get_file_path(filename):
    original_filename = filename
    nowTime = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (nowTime, original_filename)
    return os.path.join('uploads/', filename)


class Brand(models.Model):
    name = models.CharField(max_length=250, null=False, blank=False, default="Generic")
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    slug = models.CharField(max_length=250, null=False, blank=False)
    name = models.CharField(max_length=250, null=False, blank=True)
    image = models.ImageField(upload_to='category/', null=True, blank=True, storage=MediaStorage())
    description = models.TextField(max_length=600, null=False, blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    meta_title = models.CharField(max_length=150, null=True, blank=True)
    meta_keywords = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=250, blank=True)
    description = models.TextField(max_length=600, blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    original_price = models.FloatField(blank=False)
    selling_price = models.FloatField(blank=False)
    status = models.BooleanField(default=False, help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default=False, help_text="0=default, 1=Trending")
    tag = models.CharField(max_length=150, blank=False)
    meta_title = models.CharField(max_length=150, blank=True)
    meta_keywords = models.CharField(max_length=150, blank=True)
    meta_description = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    preorder_item = models.BooleanField(default=False)
    preorder_end_date = models.DateField(null=True, blank=True)
    preorder_arrival_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True, storage=MediaStorage())
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.PositiveIntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, null=False, blank=False)
    email = models.EmailField(max_length=150, null=False)
    phone = models.PositiveIntegerField(null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    REGIONS_CHOICES = (
        ('Ashanti Region', 'Ashanti Region'),
        ('Brong-Ahafo Region', 'Brong-Ahafo Region'),
        ('Central Region', 'Central Region'),
        ('Eastern Region', 'Eastern Region'),
        ('Greater Accra Region', 'Greater Accra Region'),
        ('Northern Region', 'Northern Region'),
        ('Oti Region', 'Oti Region'),
        ('Upper East Region', 'Upper East Region'),
        ('Upper West Region', 'Upper West Region'),
        ('Volta Region', 'Volta Region'),
        ('Western Region', 'Western Region'),
        ('Western North Region', 'Western North Region'),
    )
    region = models.CharField(max_length=150, null=False, blank=False, choices=REGIONS_CHOICES)
    country = models.CharField(max_length=150, null=True, blank=True)
    pincode = models.CharField(max_length=150, null=True, blank=True)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=True)
    payment_id = models.CharField(max_length=250, null=True, blank=True)
    order_statuses = (
        ('Processing', 'Processing'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled')
    )
    status = models.CharField(max_length=50, choices=order_statuses, default="Processing")
    customer_mark_as_received = models.BooleanField(default=False)
    message = models.TextField(null=True)
    tracking_number = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.user} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    tracking_number = models.CharField(max_length=150, null=True)
    quantity = models.PositiveIntegerField(null=False)
    choices = (
        ('Delivered', 'Delivered'),
        ('Arrived', 'Arrived')
    )
    preorder_order_item_status = models.CharField(max_length=250, null=True, choices=choices)

    def __str__(self):
        return f"{self.order.tracking_number} - {self.order.user} - {self.order.full_name}"


class WalletTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    choices = (
        ("Debit", "Debit"),
        ("Credit", "Credit"),
    )
    transaction_type = models.CharField(max_length=250, null=True, blank=True, choices=choices)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_use = models.CharField(max_length=250, null=True, blank=True)
    transaction_amount = models.FloatField(null=False)
    new_balance = models.FloatField(null=True)
