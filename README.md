# co-novel

一个用AI辅助写小说的助手。

## 项目结构

- `backend/` - 后端服务
- `frontend/` - 前端应用
- `docs/` - 文档

## 技术栈

- 后端: Python, FastAPI
- 前端: Vue, Element Plus
- 数据库: SQLite
- AI: OpenAI API

## 开发

### 环境设置

#### 前端

1. 安装依赖:

```bash
pnpm install
```

2. 启动开发服务器:

```bash
pnpm dev
```

#### 后端

1. 安装 [uv](https://github.com/astral-sh/uv) 包管理器
2. 安装依赖:

```bash
uv sync
```

3. 启动开发服务器:

```bash
uv run python -m main
```

## 部署

部署到 [Railway](https://railway.app) 或 [Render](https://render.com)。
