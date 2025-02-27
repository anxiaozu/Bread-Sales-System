from django.db import models
from django.urls import reverse
import os
from django.core.exceptions import ValidationError

def bread_image_upload_path(instance, filename):
    # 获取文件扩展名

    ext = os.path.splitext(filename)[1]
    # 构造新的文件名，这里使用面包的名称
    new_filename = f'{instance.name}{ext}'
    print(os.path.join('bread_images/', new_filename))
    return os.path.join('bread_images/', new_filename)

class Bread(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField(default=0)
    # image = models.ImageField(upload_to='bread_images/', blank=True, null=True)
    image = models.ImageField(upload_to=bread_image_upload_path, blank=True, null=True)
    HARDNESS_CHOICES = [
        ('soft', '软乎'),
        ('moderate', '适中'),
        ('hardish', '偏硬'),
        ('hard', '硬'),
    ]
    hardness = models.CharField(max_length=10, choices=HARDNESS_CHOICES, default='moderate')
    # 新增糖度字段，使用 DecimalField 存储百分比
    sugar_content = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def clean(self):
        if self.stock < 0:
            raise ValidationError({'stock': '库存数量不能为负数。'})

    def get_absolute_url(self):
        return reverse('bread_detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        # 确保默认权限被创建
        default_permissions = ('add', 'change', 'delete', 'view')
        # 自定义权限示例
        permissions = [
            ('can_view_special_bread', 'Can view special bread'),  # 自定义权限，用于查看特殊面包
        ]

class Category(models.Model):
    name = models.CharField(max_length=100)
    breads = models.ManyToManyField(Bread, related_name="categories")  # 🔹 重新添加多对多关系

    def __str__(self):
        return self.name


    class Meta:
        # 确保默认权限被创建
        default_permissions = ('add', 'change', 'delete', 'view')
        # 自定义权限示例
        permissions = [
            ('can_manage_category', 'Can manage category'),  # 自定义权限，用于管理分类
        ]