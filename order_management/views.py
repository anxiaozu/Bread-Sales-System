from django.shortcuts import render, redirect
from.models import Order
from bread_management.models import Bread
from user_management.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required



def order_success(request):
    return render(request, 'order_management/order_success.html')

@login_required(login_url='login')
def order_query(request):
    # 获取当前登录用户的所有订单
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_management/order_query.html', {'orders': orders})

# 使用 login_required 装饰器确保只有登录用户可以访问该视图
# @login_required(login_url='login')
# def cancel_order(request, order_id):
#     # 获取指定 id 的订单，如果不存在则返回 404 错误
#     order = get_object_or_404(Order, id=order_id)
#     # 检查订单的用户是否为当前登录用户
#     if order.user == request.user:
#         # 获取订单关联的面包对象
#         bread = order.bread
#         # 增加面包的库存数量
#         bread.stock += order.quantity
#         # 保存面包对象的更改
#         bread.save()
#         # 删除订单
#         order.delete()
#         # 重定向到订单查询页面
#         return redirect('order_query')
#     else:
#         # 如果订单的用户不是当前登录用户，重定向到登录页面
#         return redirect('login')
@login_required(login_url='login')
def place_order(request, bread_id):
    try:
        bread = get_object_or_404(Bread, id=bread_id)
        quantity = int(request.POST.get('quantity', 1))

        # 检查库存是否足够
        if bread.stock >= quantity:
            total_price = bread.price * quantity
            order = Order.objects.create(
                user=request.user,
                bread=bread,
                quantity=quantity,
                total_price=total_price
            )
            bread.stock -= quantity
            bread.save()

            # 标记订单为已处理
            order.is_processed = True
            order.save()

            return redirect('order_success')
        else:
            # 库存不足，返回错误信息或页面
            return render(request, 'order_management/stock_insufficient.html')
    except ValueError:
        # 处理 quantity 转换为整数时的错误
        return render(request, 'order_management/invalid_quantity.html')



from user_management.models import Wallet
@login_required(login_url='login')
def order_query(request):
    # 获取当前登录用户的所有订单
    orders = Order.objects.filter(user=request.user)

    try:
        # 获取用户的钱包对象
        wallet = Wallet.objects.get(user=request.user)
        user_balance = wallet.balance
    except Wallet.DoesNotExist:
        user_balance = 0.00
    print("***************")
    print("传递给用户的余额", user_balance)

    if request.method == 'POST':
        # 获取选中的订单 ID 列表
        order_ids = request.POST.getlist('order_ids')
        print("---------------")
        print(order_ids)
        total_price = 0
        # 计算选中订单的总价
        for order_id in order_ids:
            order = get_object_or_404(Order, id=order_id)
            total_price += order.total_price

        try:
            wallet = Wallet.objects.get(user=request.user)
            if wallet.balance >= total_price:
                # 扣除钱包余额
                wallet.balance -= total_price
                wallet.save()
                for order_id in order_ids:
                    order = get_object_or_404(Order, id=order_id)
                    # 增加面包的库存数量
                    bread = order.bread
                    bread.stock += order.quantity
                    bread.save()
                    # 删除订单
                    order.delete()
                return redirect('order_query')
            else:
                return render(request, 'order_management/order_query.html', {
                    'orders': orders,
                    'user_balance': user_balance,
                    'error': '余额不足，请联系管理员充值'
                })
        except Wallet.DoesNotExist:
            return render(request, 'order_management/order_query.html', {
                'orders': orders,
                'user_balance': user_balance,
                'error': '钱包不存在，请联系管理员'
            })

    return render(request, 'order_management/order_query.html', {'orders': orders, 'user_balance': user_balance})


import logging
logger = logging.getLogger(__name__)

@login_required(login_url='login')
def cancel_order(request, order_id):
    try:
        # 获取指定 id 的订单，如果不存在则返回 404 错误
        order = get_object_or_404(Order, id=order_id)

        # 检查订单的用户是否为当前登录用户
        if order.user == request.user:
            # 获取订单关联的面包对象
            bread = order.bread

            try:
                # 增加面包的库存数量
                bread.stock += order.quantity
                # 保存面包对象的更改
                bread.save()

                # 删除订单
                order.delete()

                # 记录成功日志
                logger.info(f"Order {order_id} has been successfully cancelled by user {request.user.id}")

                # 重定向到订单查询页面
                return redirect('order_query')
            except Exception as e:
                # 记录错误日志
                logger.error(f"Error occurred while cancelling order {order_id}: {str(e)}")
                # 可以根据实际情况返回错误页面
                return render(request, 'order_management/cancel_error.html', {'error': '取消订单时出现错误，请稍后再试。'})
        else:
            # 如果订单的用户不是当前登录用户，重定向到登录页面
            return redirect('login')
    except Exception as e:
        # 记录错误日志
        logger.error(f"Error occurred while retrieving order {order_id}: {str(e)}")
        # 可以根据实际情况返回错误页面
        return render(request, 'order_management/cancel_error.html', {'error': '获取订单信息时出现错误，请稍后再试。'})