from django.urls import path
from. import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('wallet/', views.wallet_view, name='wallet'),
    path('recharge_wallet/', views.recharge_wallet, name='recharge_wallet'),
    path('recharge_wallet_admin/<int:user_id>/', views.recharge_wallet_admin, name='recharge_wallet_admin'),
    path('update_bread_stock/<int:bread_id>/', views.update_bread_stock, name='update_bread_stock'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('bread_home/', views.home, name='bread_home'),  # 确保 name 参数为 'bread_home'
    # 可添加更多用户管理相关的 URL，如用户信息更新、注销等的 URL
]+ static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])