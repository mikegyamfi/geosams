from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views
from .auth import authViews
from .shop import shopViews

urlpatterns = [
                  path('', views.home, name="home"),
                  path('shop', shopViews.shop_home_collections, name="shop"),
                  path('services', views.services, name='services'),
                  path('services/mtn', views.mtn, name='mtn'),
                  path('services/airtel-tigo/', views.airtel_tigo, name='airtel-tigo'),
                  path('services/mtn/', views.mtn, name='mtn'),
                  path('history/airtel-tigo', views.history, name='history'),
                  path('history/wallet', views.wallet_history, name='wallet_history'),
                  path('history/api_wallet', views.api_wallet_history, name='api_wallet_history'),
                  path('history/telecel_api_wallet', views.telecel_api_wallet_history,
                       name='telecel_api_wallet_history'),
                  path('services/big_time/', views.big_time, name='big_time'),
                  path('services/afa/', views.afa_registration, name='afa'),
                  path('history/mtn', views.mtn_history, name="mtn-history"),
                  path('history/big_time', views.big_time_history, name="bt-history"),
                  path('history/afa', views.afa_history, name="afa-history"),
                  path('verify_transaction/<str:reference>/', views.verify_transaction, name="verify_transaction"),

                  path('services/voda/', views.voda, name='voda'),
                  path('history/voda', views.voda_history, name="voda-history"),
                  path('voda_admin/<str:status>', views.admin_voda_history, name='voda_admin'),
                  path('voda_excel_status/<str:status>/<str:to_change_to>', views.voda_change_excel_status,
                       name='voda_excel_status'),
                  path('voda_mark_as_sent/<int:pk>', views.voda_mark_as_sent, name='voda_mark_as_sent'),
                  path('voda_pay_with_wallet/', views.voda_pay_with_wallet, name='voda_pay_with_wallet'),

                  path('mtn_admin/<str:status>', views.admin_mtn_history, name='mtn_admin'),
                  path('excel_status/<str:status>/<str:to_change_to>', views.change_excel_status, name='excel_status'),

                  path('mark_as_sent/<int:pk>', views.mark_as_sent, name='mark_as_sent'),
                  path('bt_admin', views.admin_bt_history, name='bt_admin'),
                  path('afa_admin', views.admin_afa_history, name='afa_admin'),
                  path('bt_mark_as_sent/<int:pk>', views.bt_mark_as_sent, name='bt_mark_as_sent'),
                  path('afa_mark_as_sent/<int:pk>', views.afa_mark_as_sent, name='afa_mark_as_sent'),

                  path('import_thing', views.populate_custom_users_from_excel, name="import_users"),
                  path('delete', views.delete_custom_users, name='delete'),

                  path('credit_user', views.credit_user, name='credit_user'),
                  path('pay_with_wallet/', views.pay_with_wallet, name='pay_with_wallet'),
                  path('mtn_pay_with_wallet/', views.mtn_pay_with_wallet, name='mtn_pay_with_wallet'),
                  path('big_time_pay_with_wallet/', views.big_time_pay_with_wallet, name='big_time_pay_with_wallet'),
                  path('afa_pay_with_wallet/', views.afa_registration_wallet, name='afa_pay_with_wallet'),
                  path('hubtel_webhook', views.hubtel_webhook, name='hubtel_webhook'),
                  path('agent_registration', views.register_as_agent, name='register_agent'),
                  path('agent_registration_wallet', views.register_as_agent_wallet, name='register_agent_wallet'),

                  path('topup-info', views.topup_info, name='topup-info'),
                  path("request_successful/<str:reference>", views.request_successful, name='request_successful'),
                  path('elevated/topup-list', views.topup_list, name="topup_list"),
                  path('credit/<str:reference>', views.credit_user_from_list, name='credit'),

                  path('api/initiate_mtn_transaction', views.initiate_mtn_transaction, name='mtn_transaction'),
                  path('api/initiate_telecel_transaction', views.initiate_telecel_transaction,
                       name='telecel_transaction'),

                  path('login', authViews.login_page, name='login'),
                  path('signup', authViews.sign_up, name='signup'),
                  path('logout', authViews.logout_user, name="logout"),
                  path("password_reset/", views.password_reset_request, name="password_reset"),
                  path('terms_and_conditions', views.t_and_c, name='t_and_c'),

                  path('paystack_webhook', views.paystack_webhook, name='paystack_webhook'),
                  path('cancel_mtn_transaction/<int:pk>', views.cancel_mtn_transaction, name='cancel_mtn_transaction'),
                  path('admin_cancel_mtn_transaction/<int:pk>', views.admin_cancel_mtn_transaction,
                       name='admin_cancel_mtn_transaction'),

                  path('cancel_telecel_transaction/<int:pk>', views.cancel_voda_transaction,
                       name='cancel_telecel_transaction'),
                  path('admin_cancel_telecel_transaction/<int:pk>', views.admin_cancel_voda_transaction,
                       name='admin_cancel_telecel_transaction'),
                  path('check_phone_number/', views.check_phone_number, name='check_phone_number'),

                  path('elevated/profit_calculator', views.profit_home, name='profit_home'),
                  path('elevated/profit/<str:channel>', views.channel_profit, name='channel_profit'),

                  ##################################################################################################################
                  path('shop/', shopViews.shop_home_collections, name='shop'),
                  path('<str:category_name>/products', shopViews.collection_products, name='collection_products'),
                  path('<str:category_name>/<str:prod_name>/details', shopViews.product_details,
                       name='product_details'),

                  path('add-to-cart', shopViews.add_to_cart, name='add_to_cart'),
                  path('cart', shopViews.viewcart, name='cart'),
                  path('update-cart', shopViews.update_cart, name='update_cart'),
                  path('delete-cart-item', shopViews.delete_cart_item, name='delete_cart_item'),

                  path('checkout', shopViews.checkout, name='checkout'),
                  path('my-orders', shopViews.orders, name='orders'),
                  path('view-order/<str:t_no>', shopViews.view_order, name='view_order'),

                  path('elevated/admin_orders', shopViews.admin_orders, name='admin_orders'),
                  path('elevated/change_order_stat/<str:t_no>/<str:stat>', shopViews.change_order_status,
                       name='change_order_stat'),

                  path('product-list', shopViews.product_list_ajax),
                  path('search-product', shopViews.search_product, name="search-product"),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
