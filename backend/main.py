# co-novel - 后端主文件
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import ai

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
