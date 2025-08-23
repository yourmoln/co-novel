# co-novel - AI相关API路由
from fastapi import APIRouter, Depends
from typing import Dict, Any
from services.ai_service import AIService

# 创建API路由器
router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)

# AI服务实例
ai_service = AIService()

@router.get("/health")
async def ai_health():
    """AI服务健康检查"""
    return {"status": "healthy", "service": "AI"}

@router.post("/generate-content")
async def generate_content(prompt: str, max_tokens: int = 500):
    """生成小说内容"""
    content = ai_service.generate_novel_content(prompt, max_tokens)
    return {"content": content}

@router.post("/generate-title")
async def generate_title(genre: str, theme: str):
    """生成小说标题"""
    title = ai_service.generate_novel_title(genre, theme)
    return {"title": title}

@router.post("/suggestions")
async def get_suggestions(current_content: str, suggestion_type: str):
    """获取AI建议"""
    suggestions = ai_service.get_ai_suggestions(current_content, suggestion_type)
    return {"suggestions": suggestions}
