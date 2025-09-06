# co-novel - 错误处理和日志记录工具
import logging
import traceback
from typing import Any, Dict, Optional
from datetime import datetime
from functools import wraps

from fastapi import HTTPException
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """错误详情模型"""
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime
    trace_id: Optional[str] = None


class APIError(Exception):
    """自定义API错误"""
    def __init__(self, code: str, message: str, status_code: int = 500, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(message)


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """设置日志记录器"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 文件处理器
        file_handler = logging.FileHandler('logs/app.log', encoding='utf-8')
        file_handler.setLevel(level)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        logger.setLevel(level)
    
    return logger


def error_handler(logger: logging.Logger):
    """错误处理装饰器"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except APIError as e:
                logger.error(f"API Error in {func.__name__}: {e.code} - {e.message}")
                raise HTTPException(
                    status_code=e.status_code,
                    detail={
                        "code": e.code,
                        "message": e.message,
                        "details": e.details,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except ValueError as e:
                logger.error(f"Validation Error in {func.__name__}: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "VALIDATION_ERROR",
                        "message": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except Exception as e:
                logger.error(f"Unexpected Error in {func.__name__}: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "code": "INTERNAL_ERROR",
                        "message": "Internal server error",
                        "timestamp": datetime.now().isoformat()
                    }
                )
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except APIError as e:
                logger.error(f"API Error in {func.__name__}: {e.code} - {e.message}")
                raise HTTPException(
                    status_code=e.status_code,
                    detail={
                        "code": e.code,
                        "message": e.message,
                        "details": e.details,
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except ValueError as e:
                logger.error(f"Validation Error in {func.__name__}: {str(e)}")
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "VALIDATION_ERROR",
                        "message": str(e),
                        "timestamp": datetime.now().isoformat()
                    }
                )
            except Exception as e:
                logger.error(f"Unexpected Error in {func.__name__}: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "code": "INTERNAL_ERROR",
                        "message": "Internal server error",
                        "timestamp": datetime.now().isoformat()
                    }
                )
        
        # 根据函数类型返回相应的包装器
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def log_performance(logger: logging.Logger):
    """性能监控装饰器"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = datetime.now()
            try:
                result = await func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"Function {func.__name__} completed in {duration:.2f}s")
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {str(e)}")
                raise
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.info(f"Function {func.__name__} completed in {duration:.2f}s")
                return result
            except Exception as e:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()
                logger.error(f"Function {func.__name__} failed after {duration:.2f}s: {str(e)}")
                raise
        
        # 根据函数类型返回相应的包装器
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class RequestValidator:
    """请求验证器"""
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str) -> str:
        """验证字段非空"""
        if not value or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()
    
    @staticmethod
    def validate_length(value: str, field_name: str, min_length: int = 1, max_length: int = 1000) -> str:
        """验证字段长度"""
        if len(value) < min_length:
            raise ValueError(f"{field_name} must be at least {min_length} characters")
        if len(value) > max_length:
            raise ValueError(f"{field_name} must be at most {max_length} characters")
        return value
    
    @staticmethod
    def validate_range(value: int, field_name: str, min_value: int = 1, max_value: int = 100) -> int:
        """验证数值范围"""
        if value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}")
        if value > max_value:
            raise ValueError(f"{field_name} must be at most {max_value}")
        return value


# 创建全局日志记录器
app_logger = setup_logger("co-novel")
api_logger = setup_logger("co-novel.api")
ai_logger = setup_logger("co-novel.ai")
data_logger = setup_logger("co-novel.data")