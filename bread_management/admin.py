from django.contrib import admin
from .models import Bread, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    filter_horizontal = ("breads",)  # 🔹 允许在 Django Admin 里选择面包

@admin.register(Bread)
class BreadAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
    filter_horizontal = ("categories",)  # 🔹 让 Django Admin 提供多选框
