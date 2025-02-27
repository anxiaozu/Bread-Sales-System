import os
from pathlib import Path

# 构建路径辅助函数
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全密钥，应该使用一个随机字符串
SECRET_KEY = 'your_secret_key_here'

# 调试模式，开发时为 True，部署时为 False
DEBUG = True

# 允许访问的主机
ALLOWED_HOSTS = []

# 安装的应用程序
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 你的应用
    'bread_management',
    'user_management',
    'order_management',
    'django_extensions',
    # 'wallet',
]

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 根 URL 配置
ROOT_URLCONF = 'bread_sales_project.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'bread_management' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# 国际化
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# 静态文件配置
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 媒体文件配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# 静态文件存储引擎，可根据需要修改
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# 登录重定向 URL
LOGIN_REDIRECT_URL = 'bread_list'

# 注销重定向 URL
LOGOUT_REDIRECT_URL = 'home'

# 会话配置
SESSION_SAVE_EVERY_REQUEST = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 使用数据库存储会话
SESSION_COOKIE_NAME = 'my_session_cookie'  # 会话 Cookie 名称
SESSION_COOKIE_AGE = 1209600  # 会话 Cookie 过期时间，2 周
SESSION_COOKIE_SECURE = False  # 开发环境下可设置为 False，生产环境建议设置为 True
SESSION_COOKIE_HTTPONLY = True  # 防止 JavaScript 访问会话 Cookie
# SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存会话
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 浏览器关闭时会话是否过期

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'  # 你的 SMTP 服务器地址
EMAIL_PORT = 587  # SMTP 服务器端口
EMAIL_USE_TLS = True  # 是否使用 TLS 加密
EMAIL_HOST_USER = 'm18091973986@163.com'  # 你的邮箱地址
EMAIL_HOST_PASSWORD = 'lym001125@'  # 你的邮箱密码