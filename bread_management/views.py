from django.shortcuts import render, get_object_or_404, redirect
from .models import Bread
from .forms import BreadForm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.template.loader import get_template
from django.contrib.auth.models import User

def home(request):
    return render(request, 'bread_management/bread_home.html')

def bread_list(request):
    # 按照面包名称进行排序
    try:
        template = get_template('bread_management/bread_list.html')
    except Exception as e:
        print("❌ 模板加载失败！", e)
    breads_list = Bread.objects.all().order_by('name')  # 获取所有面包
    print("数据库中的面包数量:", breads_list.count())  # 打印面包数据数量

    paginator = Paginator(breads_list, 10)  # 每页显示10个面包信息
    page_number = request.GET.get('page')
    if page_number and not page_number.isdigit():
        # 如果页码不是数字，默认为第一页
        page_number = 1

    breads = paginator.get_page(page_number)
    print("当前页面的面包数据:", list(breads))

    # 判断用户是否有管理面包的权限
    is_admin = request.user.has_perm('bread_management.change_bread')

    return render(request, 'bread_management/bread_list.html', {'breads': breads, 'is_admin': is_admin})


def bread_detail(request, bread_id):
    bread = get_object_or_404(Bread, id=bread_id)
    return render(request, 'bread_management/bread_detail.html', {'bread': bread})

@login_required
@permission_required('bread_management.add_bread')
def add_bread(request):
    if request.user.has_perm('bread_management.add_bread'):
        if request.method == 'POST':
            form = BreadForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('bread_list')
        else:
            form = BreadForm()
        return render(request, 'bread_management/add_bread.html', {'form': form})
    else:
        return redirect('bread_list')


@login_required
@permission_required('bread_management.change_bread')
def update_bread(request, bread_id):
    bread = get_object_or_404(Bread, id=bread_id)
    if request.method == 'POST':
        form = BreadForm(request.POST, request.FILES, instance=bread)
        if form.is_valid():
            form.save()
            return redirect('bread_list')
    else:
        form = BreadForm(instance=bread)
    return render(request, 'bread_management/update_bread.html', {'form': form})

@login_required
@permission_required('bread_management.delete_bread')
def delete_bread(request, bread_id):
    bread = get_object_or_404(Bread, id=bread_id)
    if request.method == 'POST':
        # 删除面包对象
        bread.delete()
        return redirect('bread_list')
    return render(request, 'bread_management/confirm_delete.html', {'bread': bread})


from bread_management.recommendation import recommend_bread_knn

def user_home(request):
    """
    处理用户主页的视图函数
    """
    if request.user.is_authenticated:
        # 获取推荐面包和面包列表
        recommended_breads = recommend_bread_knn(request.user.id)
        print(request.user.id)
        print(recommended_breads)
        all_breads = Bread.objects.all()
        return render(request, 'user_management/user_home.html', {'recommended_breads': recommended_breads, 'all_breads': all_breads})
    else:
        # 如果用户未登录，重定向到登录页面
        from django.shortcuts import redirect
        return redirect('login')