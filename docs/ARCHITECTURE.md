# co-novel 架构文档

## 项目概述

co-novel 是一个用AI辅助写小说的助手。它结合了现代Web技术与AI能力，为用户提供创作小说的辅助工具。

## 项目结构

```
.
├── backend/     # 后端服务
├── frontend/    # 前端应用
├── docs/        # 文档
└── README.md    # 项目介绍
```

## 技术栈

- **后端**: Python, FastAPI
- **前端**: Vue 3, Element Plus, Vite
- **数据库**: SQLite
- **AI**: OpenAI API

## 后端架构

### 主要组件

1. **FastAPI 应用**: 提供 RESTful API 接口
2. **路由管理**: 处理各种API请求
3. **中间件**: 包括CORS支持等
4. **数据模型**: 定义数据库模型和数据结构

### API 设计

- `/` - 根路由，返回欢迎信息
- `/health` - 健康检查
- `/api/novel` - 小说相关API
- `/api/ai` - AI相关API

## 前端架构

### 主要组件

1. **Vue 3 应用**: 使用Composition API
2. **Element Plus**: UI组件库
3. **Vue Router**: 路由管理
4. **Axios**: HTTP客户端

### 页面结构

1. **首页**: 项目介绍和功能概览
2. **创作页面**: 小说创作界面
3. **AI助手**: AI辅助创作功能
4. **历史记录**: 小说历史记录查看

## 数据库设计

使用SQLite数据库存储用户数据和小说内容。

## AI集成

集成OpenAI API，提供智能创作辅助功能。
