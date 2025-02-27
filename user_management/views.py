from django.contrib.auth.models import User
from.models import Profile
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        age_str = request.POST.get('age', '')
        address = request.POST.get('address', '')
        phone = request.POST.get('phone', '')
        preferences = request.POST.get('preferences','')
        # 检查年龄是否为有效的整数
        try:
            age = int(age_str) if age_str else 0
        except ValueError:
            return render(request, 'user_management/register.html', {'error': '请输入有效的年龄'})

        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return render(request, 'user_management/register.html', {'error': '该用户名已被使用，请选择其他用户名'})
        # 创建 User 对象
        user = User.objects.create_user(username=username, email=email, password=password)
        try:
            # 检查是否已经存在与该 User 对象关联的 Profile 对象
            profile, created = Profile.objects.get_or_create(
                user=user,
                defaults={
                    'age': age,
                    'address': address,
                    'phone': phone,
                    'preferences':preferences
                }
            )
            if not created:
                # 如果 Profile 对象已经存在，更新其信息
                profile.age = age
                profile.address = address
                profile.phone = phone
                profile.preferences = preferences
                profile.save()
        except Exception as e:
            # 处理创建 Profile 对象时的异常，例如打印错误信息或采取其他措施
            print(f"创建 Profile 对象时出现错误: {e}")
            return render(request, 'user_management/register.html', {'error': '注册失败，请稍后重试'})
        return redirect('login')
    return render(request, 'user_management/register.html')



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from bread_management.recommendation import recommend_bread_knn
from urllib.parse import urlparse

def custom_is_safe_url(url, allowed_hosts):
    try:
        parsed_url = urlparse(url)
        if not parsed_url.netloc:
            return True
        return parsed_url.netloc in allowed_hosts
    except ValueError:
        return False



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # 用户认证成功，登录用户
            login(request, user)
            # 获取 next 参数
            next_url = request.POST.get('next', request.GET.get('next'))
            if next_url and custom_is_safe_url(url=next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            else:
                if user.is_staff:
                    # 管理员登录，跳转到管理员仪表盘
                    return redirect('admin_dashboard')
                else:
                    # 获取推荐面包和面包列表
                    recommended_breads = recommend_bread_knn(user.id)
                    from bread_management.models import Bread  # 假设面包模型在这个地方
                    all_breads = Bread.objects.all()
                    return render(request, 'user_management/user_home.html', {'recommended_breads': recommended_breads, 'all_breads': all_breads})
        else:
            # 用户认证失败，返回登录页面并显示错误信息
            return render(request, 'user_management/login.html', {'error': '用户名或密码错误'})
    # 如果是 GET 请求，直接渲染登录页面
    return render(request, 'user_management/login.html')

# 新增管理员充值功能
@staff_member_required(login_url='login')
def recharge_wallet_admin(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        wallet = Wallet.objects.get(user=user)
    except (User.DoesNotExist, Wallet.DoesNotExist):
        return render(request, 'user_management/recharge_wallet.html', {'error': '用户或钱包不存在'})

    if request.method == 'POST':
        amount_str = request.POST.get('amount', '0')
        try:
            amount = Decimal(amount_str)
            if amount > 0:
                with transaction.atomic():
                    wallet.balance += amount
                    wallet.save()
                    # 创建并保存充值记录
                    RechargeRecord.objects.create(wallet=wallet, amount=amount)
                return redirect('wallet')
        except ValueError:
            pass

    return render(request, 'user_management/recharge_wallet_admin.html', {'wallet': wallet, 'user': user})

# 新增面包库存的添加和更新功能
@staff_member_required(login_url='login')
def update_bread_stock(request, bread_id):
    from bread_management.models import Bread  # 假设面包模型在这个地方
    bread = get_object_or_404(Bread, id=bread_id)
    if request.method == 'POST':
        new_stock_str = request.POST.get('new_stock')
        try:
            new_stock = int(new_stock_str)
            bread.stock = new_stock
            bread.save()
            return redirect('bread_list')
        except ValueError:
            return render(request, 'bread_management/update_bread_stock.html', {'bread': bread, 'error': '请输入有效的库存数量'})
    return render(request, 'bread_management/update_bread_stock.html', {'bread': bread})


def get_bread_list(request):
    # 处理面包列表逻辑
    from bread_management.models import Bread  # 假设面包模型在这个地方
    all_breads = Bread.objects.all()
    return render(request, 'bread_management/bread_list.html', {'all_breads': all_breads})

def user_logout(request):
    # 注销当前用户
    logout(request)
    return redirect('login')

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='login')
def admin_dashboard(request):
    # 管理员功能的逻辑
    return render(request, 'user_management/admin_dashboard.html')



from django.db import transaction
from decimal import Decimal

@login_required
def recharge_wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)

    if request.method == 'POST':
        amount_str = request.POST.get('amount', '0')
        try:
            amount = Decimal(amount_str)
            if amount > 0:
                with transaction.atomic():
                    wallet.balance += amount
                    wallet.save()
                    # 创建并保存充值记录
                    RechargeRecord.objects.create(wallet=wallet, amount=amount)
                return redirect('wallet')
        except ValueError:
            pass

    return render(request, 'user_management/recharge_wallet.html', {'wallet': wallet})

from .models import Wallet, RechargeRecord
def wallet_view(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user)

    recharge_records = RechargeRecord.objects.filter(wallet=wallet)
    print("充值记录数量:", recharge_records.count())  # 添加调试信息
    print(recharge_records)

    context = {
        'wallet': wallet,
        'recharge_records': recharge_records
    }
    print("传递给模板的上下文:", context)  # 打印上下文信息
    return render(request, 'user_management/wallet.html', context)

from django.contrib import messages
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:  # 假设管理员用户的 is_staff 属性为 True
            login(request, user)
            # 重定向到管理员功能页面，这里假设为 admin_dashboard
            return redirect('admin_dashboard')
        else:
            messages.error(request, '管理员用户名或密码错误')
    return render(request, 'user_management/admin_login.html')

from user_management.models import User
from order_management.models import Order
from django.db.models import Sum
from django.utils import timezone
def admin_dashboard(request):
    # 面包销售统计
    # 计算总面包销售数量
    total_bread_sales = Order.objects.aggregate(Sum('quantity'))['quantity__sum'] or 0
    # 找出最畅销面包
    best_selling_bread = Order.objects.values('bread__name').annotate(total_quantity=Sum('quantity')).order_by('-total_quantity').first()
    if best_selling_bread:
        best_selling_bread = best_selling_bread['bread__name']
    else:
        best_selling_bread = "暂无"

    # 用户统计
    # 计算注册用户总数
    total_users = User.objects.count()
    # 计算今日新注册用户数
    today = timezone.now().date()
    new_users_today = User.objects.filter(date_joined__date=today).count()

    # 订单统计
    # 计算总订单数量
    total_orders = Order.objects.count()
    # 计算待处理订单数量（假设订单有一个is_processed字段来标记是否处理）
    pending_orders = Order.objects.filter(is_processed=False).count()

    context = {
        'total_bread_sales': total_bread_sales,
        'best_selling_bread': best_selling_bread,
        'total_users': total_users,
        'new_users_today': new_users_today,
        'total_orders': total_orders,
        'pending_orders': pending_orders
    }

    return render(request, 'user_management/admin_dashboard.html', context)

def home(request):
    return render(request, 'bread_management/bread_home.html')