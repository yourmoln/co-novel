#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试大纲生成功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import AIService

def test_outline_generation():
    print("测试大纲生成功能...")
    
    service = AIService()
    
    try:
        # 测试普通大纲生成
        print("\n=== 测试普通大纲生成 ===")
        outline = service.generate_novel_outline('玄幻', '以最弱战最强', '《逆天传说》')
        print(f"生成的大纲:\n{outline}")
        
        # 验证大纲长度是否合理（简洁版应该比较短）
        if len(outline) < 500:  # 简洁版应该比原来的详细版短很多
            print("✅ 大纲长度合适（简洁版）")
        else:
            print("❌ 大纲可能仍然过于详细")
            
        print(f"大纲字符数: {len(outline)}")
        
        # 测试流式大纲生成（仅测试方法存在性）
        print("\n=== 测试流式大纲生成方法 ===")
        stream_generator = service.generate_novel_outline_stream('玄幻', '以最弱战最强', '《逆天传说》')
        print("✅ 流式大纲生成方法存在且可调用")
        
        # 获取前几个字符测试
        first_chunk = next(stream_generator)
        print(f"流式生成首块内容: '{first_chunk[:20]}...'")
        
    except Exception as e:
        print(f"❌ 大纲生成失败: {e}")

if __name__ == "__main__":
    test_outline_generation()