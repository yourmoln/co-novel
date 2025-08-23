# co-novel - 后端主文件

import sys,os
script_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(script_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import ai
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建FastAPI应用实例
app = FastAPI(
    title="co-novel AI小说助手",
    description="一个用AI辅助写小说的助手",
    version="0.1.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该更具体
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(ai.router)

# 根路由
@app.get("/")
async def root():
    return {"message": "欢迎使用co-novel AI小说助手"}

# 健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 环境变量检查路由
@app.get("/env-check")
async def env_check():
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY", "Not set"),
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "Not set"),
        "openai_model": os.getenv("OPENAI_MODEL", "Not set"),
        "database_url": os.getenv("DATABASE_URL", "Not set"),
        "server_host": os.getenv("SERVER_HOST", "Not set"),
        "server_port": os.getenv("SERVER_PORT", "Not set")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
