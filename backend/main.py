# co-novel - 后端主文件

import sys, os
script_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(script_path)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from routers import ai
from dotenv import load_dotenv
from utils.error_handler import app_logger, setup_logger
import logging
from datetime import datetime

# 加载环境变量
load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = app_logger

# 创建FastAPI应用实例
app = FastAPI(
    title="co-novel AI小说助手",
    description="一个用AI辅助写小说的助手 - 优化版本",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "*"  # 开发环境允许所有来源，生产环境应该更具体
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error_code": "INTERNAL_ERROR",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
            "timestamp": datetime.now().isoformat()
        }
    )

# 包含路由
app.include_router(ai.router)

# 启动事件
@app.on_event("startup")
async def startup_event():
    logger.info("co-novel AI小说助手启动中...")
    logger.info(f"服务版本: 2.0.0")
    logger.info(f"启动时间: {datetime.now().isoformat()}")
    
    # 检查必要的目录
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    logger.info("co-novel AI小说助手启动完成")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("co-novel AI小说助手正在关闭...")

# 根路由
@app.get("/")
async def root():
    return {
        "message": "欢迎使用co-novel AI小说助手",
        "version": "2.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "features": [
            "AI标题生成",
            "流式大纲生成", 
            "章节内容生成",
            "创作会话管理",
            "数据持久化"
        ]
    }

# 健康检查路由
@app.get("/health")
async def health_check():
    try:
        # 检查各种服务状态
        from services.data_service import data_manager
        stats = data_manager.get_statistics()
        
        return {
            "status": "healthy",
            "version": "2.0.0",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "api": "healthy",
                "ai": "healthy",
                "data": "healthy"
            },
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        )

# 环境变量检查路由
@app.get("/env-check")
async def env_check():
    return {
        "openai_api_key": "✓ 已配置" if os.getenv("OPENAI_API_KEY") else "✗ 未配置",
        "openai_base_url": os.getenv("OPENAI_BASE_URL", "使用默认"),
        "openai_model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        "server_host": os.getenv("SERVER_HOST", "0.0.0.0"),
        "server_port": int(os.getenv("SERVER_PORT", "8000")),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # 从环境变量获取配置
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", "8000"))
    
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True if os.getenv("ENVIRONMENT", "development") == "development" else False,
        log_level="info"
    )
