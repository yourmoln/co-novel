# co-novel - AI相关API路由
from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import json
import time
import logging

# 导入业务服务和数据模型
from services.novel_service import novel_service
from services.ai_service import AIService
from models.novel import (
    TitleGenerationRequest, OutlineGenerationRequest, ChapterGenerationRequest,
    NovelGenre, APIResponse
)

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建API路由器
router = APIRouter(
    prefix="/api/ai",
    tags=["AI"],
    responses={
        500: {"description": "Internal server error"},
        422: {"description": "Validation error"},
        400: {"description": "Bad request"}
    }
)

# AI服务实例
ai_service = AIService()

# 兼容性请求模型（保持向后兼容）
class LegacyGenerateOutlineRequest(BaseModel):
    genre: str
    theme: str
    title: str

class LegacyGenerateChapterRequest(BaseModel):
    title: str
    outline: str
    chapter_number: int = 1
    custom_title: Optional[str] = None

class LegacyGenerateContentRequest(BaseModel):
    prompt: str
    max_tokens: int = 500

class LegacyGenerateTitleRequest(BaseModel):
    genre: str
    theme: str

class GetSuggestionsRequest(BaseModel):
    current_content: str
    suggestion_type: str

# 响应模型（保持向后兼容）
class GenerateOutlineResponse(BaseModel):
    outline: str

class GenerateChapterResponse(BaseModel):
    content: str

class GenerateContentResponse(BaseModel):
    content: str

class GenerateTitleResponse(BaseModel):
    title: str

class GetSuggestionsResponse(BaseModel):
    suggestions: str

# 错误处理装饰器
from functools import wraps

def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
    return wrapper

# 流式生成帮助函数
def create_stream_generator(content_generator, content_type: str):
    """创建流式响应生成器"""
    def stream_generator():
        # 生成唯一的ID
        import uuid
        completion_id = str(uuid.uuid4()).replace("-", "")
        
        try:
            # 生成初始响应
            initial_data = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": "deepseek-ai/DeepSeek-R1",
                "choices": [{
                    "index": 0,
                    "delta": {
                        "content": None,
                        "reasoning_content": "",
                        "role": "assistant"
                    },
                    "finish_reason": None
                }],
                "system_fingerprint": "",
                "usage": {
                    "prompt_tokens": 4,
                    "completion_tokens": 0,
                    "total_tokens": 4
                }
            }
            yield f"data: {json.dumps(initial_data, ensure_ascii=False)}\n\n"
            
            # 生成内容块
            content_chunks = []
            for chunk in content_generator:
                if chunk:  # 检查chunk不为空
                    content_chunks.append(chunk)
                    # 构造响应数据
                    chunk_data = {
                        "id": completion_id,
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        "model": "deepseek-ai/DeepSeek-R1",
                        "choices": [{
                            "index": 0,
                            "delta": {
                                "content": chunk,
                                "reasoning_content": "",
                                "role": "assistant"
                            },
                            "finish_reason": None
                        }],
                        "system_fingerprint": "",
                        "usage": {
                            "prompt_tokens": 4,
                            "completion_tokens": len("".join(content_chunks)),
                            "total_tokens": 4 + len("".join(content_chunks)),
                            "completion_tokens_details": {
                                "reasoning_tokens": 0
                            }
                        }
                    }
                    yield f"data: {json.dumps(chunk_data, ensure_ascii=False)}\n\n"
            
            # 生成结束响应
            end_data = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": int(time.time()),
                "model": "deepseek-ai/DeepSeek-R1",
                "choices": [{
                    "index": 0,
                    "delta": {
                        "content": "",
                        "reasoning_content": "",
                        "role": "assistant"
                    },
                    "finish_reason": "stop"
                }],
                "system_fingerprint": "",
                "usage": {
                    "prompt_tokens": 4,
                    "completion_tokens": len("".join(content_chunks)),
                    "total_tokens": 4 + len("".join(content_chunks)),
                    "completion_tokens_details": {
                        "reasoning_tokens": 0
                    }
                }
            }
            yield f"data: {json.dumps(end_data, ensure_ascii=False)}\n\n"
            
        except Exception as e:
            logger.error(f"Stream generation error for {content_type}: {str(e)}")
            # 发送错误信息
            error_data = {
                "id": completion_id,
                "object": "error",
                "error": {
                    "message": f"{content_type} generation failed",
                    "type": "generation_error",
                    "code": "internal_error"
                }
            }
            yield f"data: {json.dumps(error_data, ensure_ascii=False)}\n\n"
    
    return stream_generator


@router.get("/health")
async def ai_health():
    """AI服务健康检查"""
    try:
        return {
            "status": "healthy", 
            "service": "AI",
            "timestamp": time.time(),
            "version": "2.0"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Service unhealthy")

@router.post("/generate-title", response_model=GenerateTitleResponse)
@handle_errors
async def generate_title(request: LegacyGenerateTitleRequest):
    """生成小说标题"""
    try:
        # 验证类型
        if request.genre not in [g.value for g in NovelGenre]:
            raise ValueError(f"Invalid genre: {request.genre}")
        
        # 转换为新的请求格式
        title_request = TitleGenerationRequest(
            genre=NovelGenre(request.genre),
            theme=request.theme,
            count=1
        )
        
        # 调用业务服务
        response = novel_service.generate_titles(title_request)
        
        if response.success and response.data:
            return {"title": response.data["titles"][0]}
        else:
            raise HTTPException(status_code=500, detail=response.message)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Title generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Title generation failed")

@router.post("/generate-content-stream")
async def generate_content_stream(request: LegacyGenerateContentRequest):
    """流式生成小说内容"""
    try:
        content_generator = ai_service.generate_novel_content_stream(request.prompt, request.max_tokens)
        stream_gen = create_stream_generator(content_generator, "content")
        return StreamingResponse(stream_gen(), media_type="text/event-stream; charset=utf-8")
    except Exception as e:
        logger.error(f"Content stream error: {str(e)}")
        raise HTTPException(status_code=500, detail="Content stream generation failed")

@router.post("/generate-outline", response_model=GenerateOutlineResponse)
@handle_errors
async def generate_outline(request: LegacyGenerateOutlineRequest):
    """生成小说大纲"""
    try:
        # 转换为新的请求格式
        outline_request = OutlineGenerationRequest(
            genre=NovelGenre(request.genre),
            theme=request.theme,
            title=request.title
        )
        
        # 调用业务服务
        response = novel_service.generate_outline(outline_request)
        
        if response.success and response.data:
            return {"outline": response.data["outline"]}
        else:
            raise HTTPException(status_code=500, detail=response.message)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Outline generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Outline generation failed")

@router.post("/generate-chapter", response_model=GenerateChapterResponse)
@handle_errors
async def generate_chapter(request: LegacyGenerateChapterRequest):
    """生成指定章节内容"""
    try:
        # 转换为新的请求格式
        chapter_request = ChapterGenerationRequest(
            title=request.title,
            outline=request.outline,
            chapter_number=request.chapter_number,
            custom_title=request.custom_title
        )
        
        # 调用业务服务
        response = novel_service.generate_chapter(chapter_request)
        
        if response.success and response.data:
            return {"content": response.data["content"]}
        else:
            raise HTTPException(status_code=500, detail=response.message)
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Chapter generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chapter generation failed")

@router.post("/generate-chapter-stream")
async def generate_chapter_stream(request: LegacyGenerateChapterRequest):
    """流式生成指定章节内容"""
    try:
        content_generator = ai_service.generate_chapter_content_stream(
            request.title, 
            request.outline, 
            request.chapter_number, 
            request.custom_title
        )
        stream_gen = create_stream_generator(content_generator, "chapter")
        return StreamingResponse(stream_gen(), media_type="text/event-stream; charset=utf-8")
    except Exception as e:
        logger.error(f"Chapter stream error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chapter stream generation failed")

@router.post("/generate-outline-stream")
async def generate_outline_stream(request: LegacyGenerateOutlineRequest):
    """流式生成小说大纲"""
    try:
        content_generator = ai_service.generate_novel_outline_stream(request.genre, request.theme, request.title)
        stream_gen = create_stream_generator(content_generator, "outline")
        return StreamingResponse(stream_gen(), media_type="text/event-stream; charset=utf-8")
    except Exception as e:
        logger.error(f"Outline stream error: {str(e)}")
        raise HTTPException(status_code=500, detail="Outline stream generation failed")

# 移除重复的标题生成路由，使用上面的generate_title函数

@router.post("/suggestions", response_model=GetSuggestionsResponse)
@handle_errors
async def get_suggestions(request: GetSuggestionsRequest):
    """获取AI建议"""
    try:
        suggestions = ai_service.get_ai_suggestions(request.current_content, request.suggestion_type)
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Suggestions generation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Suggestions generation failed")

# === 章节管理相关API ===

class SaveChapterRequest(BaseModel):
    title: str
    content: str
    chapter_number: int
    custom_title: Optional[str] = None
    genre: str
    theme: str
    outline: str

class SaveChapterResponse(BaseModel):
    success: bool
    message: str
    chapter_id: str
    novel_id: str

class ChapterSummary(BaseModel):
    chapter_id: str
    novel_id: str
    title: str
    chapter_number: int
    word_count: int
    created_at: str
    novel_title: str
    genre: str
    theme: str

@router.post("/save-chapter", response_model=SaveChapterResponse)
@handle_errors
async def save_chapter(request: SaveChapterRequest):
    """保存章节到数据库"""
    try:
        # 调用业务服务保存章节
        result = novel_service.save_chapter_new(
            title=request.title,
            content=request.content,
            chapter_number=request.chapter_number,
            custom_title=request.custom_title,
            genre=request.genre,
            theme=request.theme,
            outline=request.outline
        )
        
        if result["success"]:
            return SaveChapterResponse(
                success=True,
                message="章节保存成功",
                chapter_id=result["chapter_id"],
                novel_id=result["novel_id"]
            )
        else:
            raise HTTPException(status_code=500, detail=result["message"])
            
    except Exception as e:
        logger.error(f"Save chapter error: {str(e)}")
        raise HTTPException(status_code=500, detail="章节保存失败")

@router.get("/saved-chapters")
@handle_errors
async def get_saved_chapters():
    """获取所有已保存的章节列表"""
    try:
        chapters = novel_service.get_all_saved_chapters()
        return {
            "success": True,
            "chapters": chapters
        }
    except Exception as e:
        logger.error(f"Get saved chapters error: {str(e)}")
        raise HTTPException(status_code=500, detail="获取章节列表失败")

@router.get("/chapter/{chapter_id}")
@handle_errors
async def get_chapter_content(chapter_id: str):
    """获取特定章节的完整内容"""
    try:
        chapter_data = novel_service.get_chapter_content(chapter_id)
        if chapter_data:
            return {
                "success": True,
                "chapter": chapter_data
            }
        else:
            raise HTTPException(status_code=404, detail="章节不存在")
    except Exception as e:
        logger.error(f"Get chapter content error: {str(e)}")
        raise HTTPException(status_code=500, detail="获取章节内容失败")

@router.put("/chapter/{chapter_id}/position")
@handle_errors
async def update_chapter_position(chapter_id: str, request: dict):
    """修改章节位置"""
    try:
        new_position = request.get('new_position')
        if not new_position or not isinstance(new_position, int) or new_position < 1:
            raise HTTPException(status_code=400, detail="新位置必须是大于0的整数")
        
        success = novel_service.update_chapter_position(chapter_id, new_position)
        if success:
            return {
                "success": True,
                "message": f"章节位置已更新为第{new_position}章"
            }
        else:
            raise HTTPException(status_code=404, detail="章节不存在或更新失败")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Update chapter position error: {str(e)}")
        raise HTTPException(status_code=500, detail="修改章节位置失败")
