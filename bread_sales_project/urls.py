from django.contrib import admin
from django.urls import path, include
from bread_management.views import home
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('breads/', include('bread_management.urls')),
    path('users/', include('user_management.urls')),
    path('orders/', include('order_management.urls')),
    # path('wallet/', include('wallet.urls')),
    path('', home, name='home'),
    # path('accounts/', include('django.contrib.auth.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)