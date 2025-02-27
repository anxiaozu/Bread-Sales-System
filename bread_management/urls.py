from django.urls import path
from. import views
from bread_management.views import bread_list

# app_name = 'bread_management'

urlpatterns = [
    # 主页路由
    path('', views.home, name='home'),
    # 面包列表页路由
    path('breads/', bread_list, name='bread_list'),

    # 面包详情页路由，根据面包 ID 显示详情
    path('breads/<int:bread_id>/', views.bread_detail, name='bread_detail'),
    # 面包更新页路由，根据面包 ID 进行更新操作
    path('breads/<int:bread_id>/update/', views.update_bread, name='update_bread'),
    # 添加面包页路由
    path('breads/add/', views.add_bread, name='add_bread'),
    # 面包删除页路由，根据面包 ID 进行删除操作
    path('breads/<int:bread_id>/delete/', views.delete_bread, name='delete_bread'),
    path('user_home/', views.user_home, name='user_home'),
]