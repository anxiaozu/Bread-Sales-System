#breadd Sales System

Bread Sales System 是一个基于 Django 的面包销售系统，同时集成了基于 KNN 和 DNN 神经网络的推荐算法，能够根据用户年龄及偏好为用户推荐适合的面包产品。

## 项目特点

- **销售管理**：支持面包产品的展示、管理及销售。
- **订单管理**：实现订单生成、查询及管理功能。
- **用户管理**：提供用户注册、登录及个人信息管理功能。
- **智能推荐**：基于 KNN 算法和 DNN 神经网络，根据用户年龄和喜好生成个性化推荐。

## 项目结构

Bread-Sales-System/ ├── bread_management/ # 面包相关管理模块（如产品信息的增删改查） ├── order_management/ # 订单相关功能模块 ├── user_management/ # 用户管理模块（注册、登录、权限控制等） ├── bread_sales_project/ # Django 项目配置文件（settings、urls 等） ├── media/ # 媒体文件存放目录（例如面包图片） ├── static/ # 静态资源（CSS、JavaScript、图片等） ├── templates/ # 模板文件目录 ├── db.sqlite3 # SQLite 数据库文件 ├── manage.py # Django 管理脚本 └── locustfile.py # 使用 Locust 进行性能测试的脚本


## 安装与配置

1. **克隆仓库**

   git clone https://github.com/anxiaozu/Bread-Sales-System.git
   cd Bread-Sales-System
2.**创建虚拟环境并激活**


   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # Windows: venv\Scripts\activate
3.**安装依赖**
   pip install -r requirements.txt
4.**数据库迁移**
   python manage.py migrate
5.**运行项目**
   python manage.py runserver
   访问 http://127.0.0.1:8000/ 即可查看系统首页。

6.**智能推荐模块**
   推荐模块基于两种算法：
      KNN（最近邻算法）：根据用户的历史行为与相似用户的偏好，初步筛选合适的产品。
      DNN（深度神经网络）：进一步结合用户的年龄、行为数据等多维度信息，生成个性化推荐结果。

开发者可以在各自的业务模块中找到算法实现和数据处理逻辑，根据需要进行调优和扩展。

7.**性能测试**
   项目中包含 locustfile.py 文件，使用 Locust 进行负载测试。安装依赖后，可使用以下命令启动 Locust：
   locust -f locustfile.py
   然后访问 http://localhost:8089/ 进行测试配置和结果查看。

**贡献**
欢迎提出 issue 或者提交 pull request 改进项目。请确保在贡献前阅读项目的贡献指南（如果有）。
