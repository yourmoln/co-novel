# co-novel - AI相关API路由
from fastapi import APIRouter, Depends, Body
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
async def generate_content(prompt: str = Body(...), max_tokens: int = Body(500)):
    """生成小说内容"""
    content = ai_service.generate_novel_content(prompt, max_tokens)
    return {"content": content}

@router.post("/generate-title")
async def generate_title(genre: str = Body(...), theme: str = Body(...)):
    """生成小说标题"""
    title = ai_service.generate_novel_title(genre, theme)
    return {"title": title}

@router.post("/suggestions")
async def get_suggestions(current_content: str = Body(...), suggestion_type: str = Body(...)):
    """获取AI建议"""
    suggestions = ai_service.get_ai_suggestions(current_content, suggestion_type)
    return {"suggestions": suggestions}
