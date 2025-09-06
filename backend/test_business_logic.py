#!/usr/bin/env python3
# co-novel - 业务逻辑测试脚本

import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_data_models():
    """测试数据模型"""
    print("🧪 测试数据模型...")
    
    try:
        from models.novel import (
            NovelProject, Chapter, CreationSession, AIGenerationCache,
            NovelGenre, NovelStatus, ChapterStatus, CreationStep
        )
        
        # 测试小说项目创建
        novel = NovelProject(
            genre=NovelGenre.FANTASY,
            theme="以最弱战最强的逆袭之路"
        )
        assert novel.id is not None
        assert novel.genre == NovelGenre.FANTASY
        assert novel.status == NovelStatus.DRAFT
        print("✅ 数据模型测试通过")
        
        return True
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

def test_data_service():
    """测试数据服务"""
    print("🧪 测试数据服务...")
    
    try:
        from services.data_service import data_manager
        from models.novel import NovelGenre
        
        # 测试创建小说
        novel = data_manager.create_novel(NovelGenre.FANTASY, "测试主题")
        assert novel.id is not None
        
        # 测试获取小说
        retrieved_novel = data_manager.get_novel(novel.id)
        assert retrieved_novel is not None
        assert retrieved_novel.theme == "测试主题"
        
        # 测试创建会话
        session = data_manager.create_session(novel.id)
        assert session.novel_id == novel.id
        
        # 测试统计信息
        stats = data_manager.get_statistics()
        assert isinstance(stats, dict)
        assert "total_novels" in stats
        
        print("✅ 数据服务测试通过")
        return True
    except Exception as e:
        print(f"❌ 数据服务测试失败: {e}")
        return False

def test_ai_service():
    """测试AI服务"""
    print("🧪 测试AI服务...")
    
    try:
        from services.ai_service import AIService
        
        ai_service = AIService()
        
        # 测试标题生成（无需API）
        title = ai_service.generate_novel_title("玄幻", "测试主题")
        assert isinstance(title, str)
        assert len(title) > 0
        
        # 测试缓存功能
        from models.novel import AIGenerationCache
        cache_key = AIGenerationCache.generate_cache_key("test", theme="测试")
        assert isinstance(cache_key, str)
        assert len(cache_key) == 32  # MD5长度
        
        print("✅ AI服务测试通过")
        return True
    except Exception as e:
        print(f"❌ AI服务测试失败: {e}")
        return False

def test_business_service():
    """测试业务服务"""
    print("🧪 测试业务服务...")
    
    try:
        from services.novel_service import novel_service
        from models.novel import TitleGenerationRequest, NovelGenre
        
        # 测试标题生成
        request = TitleGenerationRequest(
            genre=NovelGenre.FANTASY,
            theme="测试主题",
            count=1
        )
        
        response = novel_service.generate_titles(request)
        assert response.success is True
        assert response.data is not None
        assert "titles" in response.data
        
        print("✅ 业务服务测试通过")
        return True
    except Exception as e:
        print(f"❌ 业务服务测试失败: {e}")
        return False

def test_frontend_types():
    """测试前端类型定义"""
    print("🧪 测试前端类型定义...")
    
    try:
        # 检查类型文件是否存在
        types_file = project_root / "frontend" / "src" / "types" / "index.d.ts"
        if types_file.exists():
            content = types_file.read_text(encoding="utf-8")
            
            # 检查关键类型定义
            required_types = [
                "NovelGenre", "NovelStatus", "ChapterStatus", 
                "CreationStep", "NovelProject", "Chapter",
                "APIResponse", "CreationState"
            ]
            
            for type_name in required_types:
                if type_name not in content:
                    raise ValueError(f"Missing type definition: {type_name}")
            
            print("✅ 前端类型定义测试通过")
            return True
        else:
            print("⚠️ 前端类型文件不存在，跳过测试")
            return True
    except Exception as e:
        print(f"❌ 前端类型定义测试失败: {e}")
        return False

def test_error_handling():
    """测试错误处理"""
    print("🧪 测试错误处理...")
    
    try:
        from utils.error_handler import APIError, RequestValidator, setup_logger
        
        # 测试自定义错误
        error = APIError("TEST_ERROR", "测试错误", 400)
        assert error.code == "TEST_ERROR"
        assert error.status_code == 400
        
        # 测试验证器
        validator = RequestValidator()
        
        # 测试非空验证
        try:
            validator.validate_not_empty("", "test_field")
            assert False, "应该抛出异常"
        except ValueError:
            pass  # 预期的异常
        
        # 测试长度验证
        result = validator.validate_length("测试", "test_field", 1, 10)
        assert result == "测试"
        
        # 测试日志设置
        logger = setup_logger("test")
        assert logger is not None
        
        print("✅ 错误处理测试通过")
        return True
    except Exception as e:
        print(f"❌ 错误处理测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始业务逻辑测试...\n")
    
    tests = [
        test_data_models,
        test_data_service,
        test_ai_service,
        test_business_service,
        test_frontend_types,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 测试执行失败: {e}\n")
    
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！业务逻辑优化成功！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关代码")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)