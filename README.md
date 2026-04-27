# 新闻资讯服务平台

新闻资讯服务平台是一个前后端分离的新闻内容服务项目，提供用户注册登录、新闻分类浏览、新闻详情、收藏管理、浏览历史、个人资料维护以及 AI 问答等功能。后端基于 FastAPI 异步栈实现接口服务，前端基于 Vue 3 与 Vite 构建移动端页面。

## 项目概述

- 后端提供统一的 RESTful API，负责用户认证、新闻数据查询、收藏与历史记录管理。
- 前端提供新闻浏览与个人中心界面，负责交互、状态管理和多语言展示。
- Redis 用于缓存分类、新闻列表、新闻详情和相关推荐等热点数据。
- MySQL 用于存储用户、新闻、收藏、历史记录及令牌信息。

## 功能特性

- 用户注册、登录、鉴权、个人资料修改、密码修改
- 新闻分类查询、新闻列表分页、新闻详情、相关推荐
- 收藏列表管理、浏览历史管理
- Redis 缓存加速热点接口访问
- 基于 Pinia 的前端状态管理
- 基于 Vue I18n 的中英文切换
- AI 问答页面接入第三方大模型接口

## 技术栈

### 后端

- FastAPI
- SQLAlchemy 2.x（异步）
- MySQL
- Redis
- Passlib + bcrypt
- Uvicorn

### 前端

- Vue 3
- Vite
- Vue Router
- Pinia
- Vant
- Vue I18n
- Axios

## 目录结构

```text
.
├── cache/                 # 缓存键封装
├── config/                # 数据库、缓存配置
├── crud/                  # 数据访问层
├── models/                # SQLAlchemy 数据模型
├── routers/               # FastAPI 路由
├── schemas/               # Pydantic 请求/响应模型
├── utils/                 # 鉴权、异常、统一响应等工具
├── 前端项目代码/            # Vue 3 前端工程
├── 数据库sql文件/          # 数据库初始化脚本
├── 说明文档/              # 接口与设计说明文档
├── main.py                # 后端应用入口
├── README.md              # 项目说明
└── requirements.txt       # 后端依赖
```

## 环境要求

- Python 3.11 及以上
- Node.js 18 及以上
- MySQL 8.0 及以上
- Redis 6.0 及以上

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd 新闻资讯服务平台
```

### 2. 创建并激活 Python 虚拟环境

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 安装后端依赖

```bash
pip install -r requirements.txt
```

### 4. 配置后端服务

启动前请根据本地环境修改以下配置文件：

- `config/db_conf.py`：MySQL 连接地址、用户名、密码、数据库名
- `config/cache_conf.py`：Redis 主机、端口、数据库编号

建议将数据库连接、缓存连接和第三方密钥迁移到环境变量管理，避免在公开仓库中提交敏感信息。

### 5. 初始化数据库

1. 在 MySQL 中创建数据库，例如 `news_app`
2. 导入脚本 `数据库sql文件/database.sql`

可使用 Navicat、DBeaver 或 MySQL 命令行工具完成初始化。

### 6. 启动后端

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

启动成功后可访问：

- API 服务地址：`http://127.0.0.1:8000`
- OpenAPI 文档：`http://127.0.0.1:8000/docs`
- ReDoc 文档：`http://127.0.0.1:8000/redoc`

### 7. 启动前端

```bash
cd 前端项目代码
npm install
npm run dev
```

如需调整前端接口地址或 AI 服务参数，请修改：

- `前端项目代码/src/config/api.js`

前端开发服务默认地址通常为：

- `http://127.0.0.1:5173`

### 8. 构建前端

```bash
cd 前端项目代码
npm run build
```

## 认证与接口约定

- 登录或注册成功后，后端返回访问令牌 `token`
- 需要登录态的接口通过请求头 `Authorization` 传递令牌
- 接口统一返回 JSON 数据，结构如下：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 主要接口模块

- 用户模块：`/api/user/*`
- 新闻模块：`/api/news/*`
- 收藏模块：`/api/favorite/*`
- 历史记录模块：`/api/history/*`

详细接口说明见 `说明文档/API接口规范文档.md`。

## 文档与数据文件

- 后端设计说明：`说明文档/项目后端设计说明文档.md`
- 接口规范文档：`说明文档/API接口规范文档.md`
- 数据库脚本：`数据库sql文件/database.sql`

## 开发与发布建议

- 不要将 `node_modules/`、`dist/`、`.idea/`、`__pycache__/` 等生成文件提交到版本库
- 在提交到公开仓库前，移除或替换数据库密码、第三方 API Key 等敏感信息
- 生产环境请关闭调试信息，收紧 CORS 白名单，并将配置迁移到环境变量

