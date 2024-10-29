# admin.py

from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.db.models import Exists, OuterRef
from django.urls import path
from django.shortcuts import redirect, get_object_or_404
from django.utils.html import format_html
from django.db import transaction as db_transaction
from django.utils import timezone
from . import models
from import_export.admin import ExportActionMixin
import logging
from django.core.mail import send_mail
from django.conf import settings

# Initialize Logger for Refund Actions
logger = logging.getLogger('refunds')

# Base Admin Class for Common Settings
class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25  # Limit records per page to improve load times
    ordering = ['-id']  # Default ordering
    search_fields = []
    list_filter = []
    list_select_related = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if self.list_select_related:
            qs = qs.select_related(*self.list_select_related)
        return qs

# RefundMixin to Add Refund Functionality
class RefundMixin:
    """
    Mixin to add refund functionality to Transaction Admins.
    """

    history_model = None  # To be set in subclass (e.g., APIUsersHistory)
    api_transaction_field = None  # To be set in subclass (e.g., 'mtn_transaction')
    refund_channel = None  # To be set in subclass (e.g., 'MTN' or 'Telecel')

    def refund_button(self, obj):
        """
        Returns a formatted HTML button to initiate a refund.
        """
        if not obj.refunded:
            return format_html(
                '<a class="button" href="{}" style="padding: 5px 10px; background-color: #dc3545; color: white; border-radius: 3px; text-decoration: none;">Refund</a>',
                f'refund/{obj.pk}/'
            )
        return format_html(
            '<span style="color: grey;">Already Refunded</span>'
        )
    refund_button.short_description = 'Action'

    def get_urls(self):
        """
        Extends the default admin URLs with a custom refund URL.
        """
        urls = super().get_urls()
        custom_urls = [
            path(
                'refund/<int:transaction_id>/',
                self.admin_site.admin_view(self.refund_view),
                name='refund-transaction',
            ),
        ]
        return custom_urls + urls

    def refund_view(self, request, transaction_id, *args, **kwargs):
        """
        Handles the refund logic when the refund button is clicked.
        """
        transaction = get_object_or_404(self.model, pk=transaction_id)

        # Check if already refunded
        if transaction.refunded:
            self.message_user(request, "This transaction has already been refunded.", level=messages.WARNING)
            return redirect('..')

        # Validate transaction amount
        if transaction.amount is None or transaction.amount <= 0:
            self.message_user(request, "Invalid transaction amount.", level=messages.ERROR)
            return redirect('..')

        try:
            with db_transaction.atomic():
                # Check if the transaction is linked to an API user
                api_history = self.history_model.objects.filter(**{self.api_transaction_field: transaction}).first()
                if api_history:
                    api_user = api_history.api_user
                    if api_user is None:
                        self.message_user(request, "No API user linked to this transaction.", level=messages.ERROR)
                        return redirect('..')

                    # Update API user's wallet balance
                    api_user.wallet_balance += transaction.amount
                    api_user.save()

                    # Create an ApiWalletTransaction record
                    models.ApiWalletTransaction.objects.create(
                        user=api_user.user,  # Assuming MTNAPIUsers.user is the CustomUser
                        transaction_type="Credit",
                        transaction_channel=self.refund_channel,
                        transaction_date=timezone.now(),
                        transaction_amount=transaction.amount,
                        new_balance=api_user.wallet_balance
                    )
                else:
                    # Refund to regular user's wallet
                    user = transaction.user
                    user.wallet += transaction.amount
                    user.save()

                    # Create a WalletTransaction record
                    models.WalletTransaction.objects.create(
                        user=user,
                        transaction_type="Credit",
                        transaction_use="Refund",
                        transaction_amount=transaction.amount,
                        new_balance=user.wallet
                    )

                # Mark the transaction as refunded
                transaction.refunded = True
                transaction.save()

                # Log the refund action
                logger.info(f"Refunded GHS{transaction.amount} to {transaction.user.username} for Transaction ID {transaction.id} at {timezone.now()}.")

                # Send email notification to the user
                send_mail(
                    subject='Transaction Refund Processed',
                    message=f"Dear {transaction.user.first_name},\n\nYour transaction with reference {transaction.reference} has been refunded.\n\nAmount: GHS{transaction.amount}\n\nThank you.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[transaction.user.email],
                    fail_silently=True,
                )

                # Provide success feedback
                self.message_user(
                    request,
                    f"Successfully refunded GHS{transaction.amount} to {transaction.user.username}.",
                    level=messages.SUCCESS
                )

        except Exception as e:
            # Handle any exceptions and provide error feedback
            self.message_user(
                request,
                f"An error occurred during refund: {str(e)}",
                level=messages.ERROR
            )
            logger.error(f"Failed to refund Transaction ID {transaction.id}: {str(e)}")

        return redirect('..')

# Custom User Admin
class CustomUserAdmin(ExportActionMixin, UserAdmin):
    list_display = ['first_name', 'last_name', 'username', 'email', 'wallet', 'phone']
    search_fields = ['username', 'email', 'phone']
    list_select_related = []
    ordering = ['username']

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Other Personal Info',
            {
                'fields': ('phone', 'wallet', 'status', 'data_bundle_access')
            }
        ),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'wallet')
        }),
    )

# MTNTransaction Admin with Refund Functionality
class MTNTransactionAdmin(RefundMixin, BaseAdmin):
    list_display = [
        'user',
        'bundle_number',
        'offer',
        'reference',
        'transaction_status',
        'transaction_date',
        'is_api_transaction',  # Indicates if related to API
        'refund_button'        # Refund button
    ]
    search_fields = ['user__username', 'reference', 'bundle_number']
    list_filter = ['transaction_status', 'transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']
    history_model = models.APIUsersHistory
    api_transaction_field = 'mtn_transaction'
    refund_channel = 'MTN'  # Set the refund channel

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(
            is_api_transaction=Exists(
                models.APIUsersHistory.objects.filter(mtn_transaction=OuterRef('pk'))
            )
        )
        return qs

    def is_api_transaction(self, obj):
        return obj.is_api_transaction
    is_api_transaction.boolean = True
    is_api_transaction.short_description = 'API Transaction'

# VodafoneTransaction Admin with Refund Functionality
class VodafoneTransactionAdmin(RefundMixin, BaseAdmin):
    list_display = [
        'user',
        'bundle_number',
        'offer',
        'reference',
        'transaction_status',
        'transaction_date',
        'refund_button'  # Added refund button to the list display
    ]
    search_fields = ['user__username', 'reference', 'bundle_number']
    list_filter = ['transaction_status', 'transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']
    history_model = models.TelecelAPIUsersHistory
    api_transaction_field = 'telecel_transaction'
    refund_channel = 'Telecel'  # Set the refund channel

# IShareBundleTransaction Admin
class IShareBundleTransactionAdmin(BaseAdmin):
    list_display = ['user', 'bundle_number', 'offer', 'reference', 'transaction_status', 'transaction_date']
    search_fields = ['user__username', 'reference', 'bundle_number']
    list_filter = ['transaction_status', 'transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']

# WalletTransaction Admin
class WalletTransactionAdmin(BaseAdmin):
    list_display = [
        'user',
        'transaction_type',
        'transaction_amount',
        'transaction_use',
        'new_balance',
        'transaction_date'
    ]
    search_fields = ['user__username', 'transaction_type']
    list_filter = ['transaction_type', 'transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']

# ApiWalletTransaction Admin
class ApiWalletTransactionAdmin(BaseAdmin):
    list_display = [
        'user',
        'transaction_type',
        'transaction_amount',
        'transaction_channel',
        'new_balance',
        'transaction_date'
    ]
    search_fields = ['user__username', 'transaction_type']
    list_filter = ['transaction_type', 'transaction_channel', 'transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']

# Payment Admin
class PaymentAdmin(BaseAdmin):
    list_display = ['user', 'reference', 'transaction_date', 'amount']
    search_fields = ['user__username', 'reference']
    list_filter = ['transaction_date']
    list_select_related = ['user']
    ordering = ['-transaction_date']

# TopUpRequest Admin
class TopUpRequestAdmin(BaseAdmin):
    list_display = ['user', 'reference', 'amount', 'date', 'status']
    search_fields = ['user__username', 'reference']
    list_filter = ['status', 'date']
    list_select_related = ['user']
    ordering = ['-date']

# Agent Registration Admin
class AgentRegAdmin(BaseAdmin):
    list_display = ['user', 'amount', 'date']
    search_fields = ['user__username', 'amount']
    list_filter = ['date']
    list_select_related = ['user']
    ordering = ['-date']

# ProductImage Inline
class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 4
    max_num = 10  # Prevent excessive inlines

# Product Admin
class ProductAdmin(BaseAdmin):
    inlines = [ProductImageInline]
    search_fields = ['name']
    list_display = ['name', 'category', 'brand', 'selling_price', 'quantity']
    list_filter = ['category', 'brand', 'status', 'trending']
    list_select_related = ['category', 'brand']
    ordering = ['name']

# Announcement Admin
class AnnouncementAdmin(BaseAdmin):
    list_display = ['message', 'active']
    search_fields = ['message']
    list_filter = ['active']
    ordering = ['-id']

# Category Admin
class CategoryAdmin(BaseAdmin):
    list_display = ['name', 'status', 'trending']
    search_fields = ['name']
    list_filter = ['status', 'trending']
    ordering = ['name']

# Order Admin
class OrderAdmin(BaseAdmin):
    list_display = ['tracking_number', 'user', 'full_name', 'status', 'created_at']
    search_fields = ['tracking_number', 'user__username', 'full_name']
    list_filter = ['status', 'created_at']
    list_select_related = ['user']
    ordering = ['-created_at']

# Register All Models with Their Respective Admin Classes
admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.MTNTransaction, MTNTransactionAdmin)
admin.site.register(models.VodafoneTransaction, VodafoneTransactionAdmin)
admin.site.register(models.IShareBundleTransaction, IShareBundleTransactionAdmin)
admin.site.register(models.WalletTransaction, WalletTransactionAdmin)
admin.site.register(models.ApiWalletTransaction, ApiWalletTransactionAdmin)
admin.site.register(models.Payment, PaymentAdmin)
admin.site.register(models.TopUpRequestt, TopUpRequestAdmin)  # Note: Ensure 'TopUpRequestt' is intentional
admin.site.register(models.AgentRegistration, AgentRegAdmin)
admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)

# Register Unmanaged Models Without Custom Admins
admin.site.register(models.IshareBundlePrice)
admin.site.register(models.MTNBundlePrice)
admin.site.register(models.AgentMTNBundlePrice)
admin.site.register(models.AgentIshareBundlePrice)
admin.site.register(models.SuperAgentMTNBundlePrice)
admin.site.register(models.BigTimeBundlePrice)
admin.site.register(models.AgentBigTimeBundlePrice)
admin.site.register(models.SuperAgentBigTimeBundlePrice)
admin.site.register(models.VodaBundlePrice)
admin.site.register(models.AgentVodaBundlePrice)
admin.site.register(models.SuperAgentVodaBundlePrice)
admin.site.register(models.APIMTNBundlePrice)
admin.site.register(models.MTNAPIUsers)
admin.site.register(models.APIUsersHistory)
admin.site.register(models.APITelecelBundlePrice)
admin.site.register(models.OrderItem)
admin.site.register(models.Cart)
admin.site.register(models.Brand)
admin.site.register(models.ProductImage)
admin.site.register(models.SuperAgentIshareBundlePrice)
admin.site.register(models.AFARegistration)
admin.site.register(models.BigTimeTransaction)
admin.site.register(models.TelecelAPIUsersHistory)  # Ensure this is only registered once
admin.site.register(models.AdminInfo)
