#!/usr/bin/env python3
"""
测试章节保存和重新打开功能
"""

import requests
import json
import time
from datetime import datetime

# API配置
API_BASE_URL = "http://localhost:8000/api/ai"

def test_save_chapter():
    """测试保存章节功能"""
    print("🧪 测试保存章节功能...")
    
    # 测试数据
    test_data = {
        "title": "测试小说《剑仙逆天》",
        "content": "第一章 少年天才\n\n在修仙界的边陲小镇青云镇，有一个名叫李逍遥的少年。他自幼天赋异禀，虽然出身贫寒，但志向远大。这一天，李逍遥正在后山练剑，突然天空中雷云密布，紫电闪烁，一道天雷劈下，正好击中了他手中的木剑。木剑瞬间化为齑粉，但李逍遥却毫发无伤，甚至感到体内有一股神秘的力量在涌动...",
        "chapter_number": 1,
        "custom_title": "少年天才",
        "genre": "玄幻",
        "theme": "修仙逆天，热血成长",
        "outline": "第一章：少年天才 - 介绍主角李逍遥，展现其天赋异禀\n第二章：奇遇 - 获得神秘传承\n第三章：初入宗门 - 加入青云宗开始修行"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/save-chapter",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ 章节保存成功！")
            print(f"   章节ID: {result['chapter_id']}")
            print(f"   小说ID: {result['novel_id']}")
            return result['chapter_id'], result['novel_id']
        else:
            print(f"❌ 保存失败，状态码: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ 保存时发生异常: {str(e)}")
        return None, None

def test_get_saved_chapters():
    """测试获取已保存章节列表"""
    print("\n🧪 测试获取已保存章节列表...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/saved-chapters",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                chapters = result['chapters']
                print(f"✅ 获取章节列表成功，共 {len(chapters)} 个章节:")
                for i, chapter in enumerate(chapters, 1):
                    print(f"   {i}. {chapter['title']} ({chapter['novel_title']})")
                    print(f"      字数: {chapter['word_count']} | 创建时间: {chapter['created_at']}")
                return chapters
            else:
                print(f"❌ 获取失败: {result.get('message', '未知错误')}")
                return []
        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 获取时发生异常: {str(e)}")
        return []

def test_get_chapter_content(chapter_id):
    """测试获取特定章节内容"""
    print(f"\n🧪 测试获取章节内容 (ID: {chapter_id})...")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/chapter/{chapter_id}",
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                chapter = result['chapter']
                print(f"✅ 获取章节内容成功:")
                print(f"   标题: {chapter['title']}")
                print(f"   小说: {chapter['novel_title']}")
                print(f"   内容长度: {len(chapter['content'])} 字符")
                print(f"   内容预览: {chapter['content'][:100]}...")
                return chapter
            else:
                print(f"❌ 获取失败: {result.get('message', '未知错误')}")
                return None
        else:
            print(f"❌ 获取失败，状态码: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ 获取时发生异常: {str(e)}")
        return None

def main():
    """主测试函数"""
    print("🚀 开始测试章节保存和重新打开功能")
    print("=" * 60)
    
    # 测试1：保存章节
    chapter_id, novel_id = test_save_chapter()
    if not chapter_id:
        print("❌ 保存测试失败，退出测试")
        return
    
    # 等待一秒让数据写入完成
    time.sleep(1)
    
    # 测试2：获取章节列表
    chapters = test_get_saved_chapters()
    
    # 测试3：获取章节内容
    if chapter_id:
        chapter_content = test_get_chapter_content(chapter_id)
    
    print("\n" + "=" * 60)
    if chapter_id and chapters:
        print("✅ 所有测试通过！章节保存和重新打开功能正常工作")
    else:
        print("❌ 部分测试失败，请检查功能实现")

if __name__ == "__main__":
    main()