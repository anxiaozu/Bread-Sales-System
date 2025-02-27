from django.urls import path
from. import views


urlpatterns = [
    # path('place_order/<int:bread_id>/', views.place_order, name='place_order'),
    path('success/', views.order_success, name='order_success'),
    path('order_query/', views.order_query, name='order_query'),
    path('place/<int:bread_id>/', views.place_order, name='place_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    # 可添加更多订单管理相关的 URL，如订单查询、订单取消等的 URL
]