# co-novel - AI相关API路由
from fastapi import APIRouter, Depends, Body, Response
from fastapi.responses import StreamingResponse
from typing import Dict, Any, List
from services.ai_service import AIService
from pydantic import BaseModel
import json
import time

# 创建API路由器
router = APIRouter(
    prefix="/api/ai",
    tags=["AI"]
)

# AI服务实例
ai_service = AIService()

# 请求模型
class GenerateOutlineRequest(BaseModel):
    genre: str
    theme: str
    title: str

class GenerateChapterRequest(BaseModel):
    title: str
    outline: str
    chapter_number: int = 1

class GenerateContentRequest(BaseModel):
    prompt: str
    max_tokens: int = 500

class GenerateTitleRequest(BaseModel):
    genre: str
    theme: str

class GetSuggestionsRequest(BaseModel):
    current_content: str
    suggestion_type: str

# 响应模型
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

@router.get("/health")
async def ai_health():
    """AI服务健康检查"""
    return {"status": "healthy", "service": "AI"}

@router.post("/generate-content", response_model=GenerateContentResponse)
async def generate_content(request: GenerateContentRequest):
    """生成小说内容"""
    content = ai_service.generate_novel_content(request.prompt, request.max_tokens)
    return {"content": content}

@router.post("/generate-content-stream")
async def generate_content_stream(request: GenerateContentRequest):
    """流式生成小说内容"""
    def stream_generator():
        # 生成唯一的ID
        import uuid
        completion_id = str(uuid.uuid4()).replace("-", "")
        
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
        for chunk in ai_service.generate_novel_content_stream(request.prompt, request.max_tokens):
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
        
        # 最终统计信息
        stats_data = {
            "id": "0",
            "object": "",
            "created": 0,
            "model": "",
            "choices": [],
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
        yield f"data: {json.dumps(stats_data, ensure_ascii=False)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream; charset=utf-8")

@router.post("/generate-outline", response_model=GenerateOutlineResponse)
async def generate_outline(request: GenerateOutlineRequest):
    """生成小说大纲"""
    outline = ai_service.generate_novel_outline(request.genre, request.theme, request.title)
    return {"outline": outline}

@router.post("/generate-chapter", response_model=GenerateChapterResponse)
async def generate_chapter(request: GenerateChapterRequest):
    """生成指定章节内容"""
    content = ai_service.generate_chapter_content(request.title, request.outline, request.chapter_number)
    return {"content": content}

@router.post("/generate-chapter-stream")
async def generate_chapter_stream(request: GenerateChapterRequest):
    """流式生成指定章节内容"""
    def stream_generator():
        # 生成唯一的ID
        import uuid
        completion_id = str(uuid.uuid4()).replace("-", "")
        
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
        for chunk in ai_service.generate_chapter_content_stream(request.title, request.outline, request.chapter_number):
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
        
        # 最终统计信息
        stats_data = {
            "id": "0",
            "object": "",
            "created": 0,
            "model": "",
            "choices": [],
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
        yield f"data: {json.dumps(stats_data, ensure_ascii=False)}\n\n"

    return StreamingResponse(stream_generator(), media_type="text/event-stream; charset=utf-8")

@router.post("/generate-outline-stream")
async def generate_outline_stream(request: GenerateOutlineRequest):
    """流式生成小说大纲"""
    def stream_generator():
        # 生成唯一的ID
        import uuid
        completion_id = str(uuid.uuid4()).replace("-", "")
        
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
        for chunk in ai_service.generate_novel_outline_stream(request.genre, request.theme, request.title):
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

    return StreamingResponse(stream_generator(), media_type="text/event-stream; charset=utf-8")

@router.post("/generate-title", response_model=GenerateTitleResponse)
async def generate_title(request: GenerateTitleRequest):
    """生成小说标题"""
    title = ai_service.generate_novel_title(request.genre, request.theme)
    return {"title": title}

@router.post("/suggestions", response_model=GetSuggestionsResponse)
async def get_suggestions(request: GetSuggestionsRequest):
    """获取AI建议"""
    suggestions = ai_service.get_ai_suggestions(request.current_content, request.suggestion_type)
    return {"suggestions": suggestions}
