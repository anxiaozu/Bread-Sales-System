from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from bread_management.models import Bread
from bread_management.views import home, bread_list, bread_detail, add_bread, update_bread, delete_bread, user_home


class BreadManagementViewsTestCase(TestCase):
    def setUp(self):
        # 创建一个测试用户
        self.user = User.objects.create_user(username='fanmo', password='001125')
        # 创建一个测试面包对象
        self.bread = Bread.objects.create(name='Test Bread', price=10.0, description='Test description', stock=10)

    def test_home_view(self):
        # 测试主页视图
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/bread_home.html')

    def test_bread_list_view(self):
        # 测试面包列表视图
        url = reverse('bread_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/bread_list.html')

    def test_bread_detail_view(self):
        # 测试面包详情视图
        url = reverse('bread_detail', args=[self.bread.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/bread_detail.html')

    def test_add_bread_view(self):
        # 测试添加面包视图（需要登录）
        self.client.login(username='testuser', password='testpassword')
        url = reverse('add_bread')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/add_bread.html')

    def test_update_bread_view(self):
        # 测试更新面包视图（需要登录）
        self.client.login(username='testuser', password='testpassword')
        url = reverse('update_bread', args=[self.bread.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/update_bread.html')

    def test_delete_bread_view(self):
        # 测试删除面包视图（需要登录）
        self.client.login(username='testuser', password='testpassword')
        url = reverse('delete_bread', args=[self.bread.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bread_management/confirm_delete.html')

    def test_user_home_view_authenticated(self):
        # 测试用户主页视图（已登录）
        self.client.login(username='testuser', password='testpassword')
        url = reverse('user_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_management/user_home.html')

    def test_user_home_view_unauthenticated(self):
        # 测试用户主页视图（未登录）
        url = reverse('user_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # 重定向到登录页面