from django import forms
from django.core.validators import MinValueValidator
from.models import Bread
from django.core.exceptions import ValidationError
import os

def validate_image_file_extension(value):
    """
    验证上传文件的扩展名是否为允许的图片格式
    """
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError('不支持的文件格式，请上传 JPG、JPEG、PNG 或 GIF 格式的图片。')

class CustomImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget.template_name = 'custom_image_field.html'

    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs.update({'class': 'custom-image-field'})
        return attrs

class BreadForm(forms.ModelForm):
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, message='价格不能为负数')],
        label='价格（元）',
        help_text='请输入面包的价格，精确到小数点后两位。',
        error_messages={
            'required': '请输入面包的价格。',
            'invalid': '请输入有效的价格。'
        }
    )
    stock = forms.IntegerField(
        validators=[MinValueValidator(0, message='库存不能为负数')],
        label='库存数量',
        help_text='请输入面包的库存数量，必须为非负整数。',
        error_messages={
            'required': '请输入面包的库存数量。',
            'invalid': '请输入有效的库存数量。'
        }
    )
    image = CustomImageField(
        label='面包图片',
        help_text='请上传面包的图片（支持 JPG、JPEG、PNG、GIF 格式）',
        validators=[validate_image_file_extension],
        required=False
    )

    class Meta:
        model = Bread
        fields = ['name', 'price', 'description', 'stock', 'image', 'hardness', 'sugar_content']
        labels = {
            'name': '面包名称',
            'description': '面包描述',
            'hardness': '面包硬度',
            'sugar_content': '面包糖度（%）',
        }
        help_texts = {
            'name': '请输入面包的名称。',
            'description': '请简要描述面包的特点和口味。',
            'hardness': '请选择面包的硬度。',
            'sugar_content': '请输入面包的糖度（百分比）。',
        }
        error_messages = {
            'name': {
                'required': '请输入面包的名称。',
                'max_length': '面包名称不能超过 %(limit_value)s 个字符。'
            },
            'description': {
                'max_length': '面包描述不能超过 %(limit_value)s 个字符。'
            }
        }