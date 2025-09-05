#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试标题生成功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService

def test_title_generation():
    print("测试标题生成功能...")
    
    service = AIService()
    
    try:
        title = service.generate_novel_title('玄幻', '以最弱战最强')
        print(f"生成的标题: {title}")
        
        # 验证标题格式
        if title.startswith('《') and title.endswith('》'):
            print("✅ 标题格式正确")
        else:
            print("❌ 标题格式错误")
            
        # 验证标题长度
        title_content = title.strip('《》')
        if 2 <= len(title_content) <= 8:
            print("✅ 标题长度合适")
        else:
            print("❌ 标题长度不合适")
            
    except Exception as e:
        print(f"❌ 标题生成失败: {e}")

if __name__ == "__main__":
    test_title_generation()