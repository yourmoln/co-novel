#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试创作流程和数据联动
"""

import requests
import json

def test_create_workflow():
    print("测试小说创作工作流程...")
    
    base_url = "http://localhost:8000/api/ai"
    
    # 模拟完整的创作流程
    workflow_data = {
        "genre": "玄幻",
        "theme": "以最弱战最强"
    }
    
    print("\n=== 步骤1: 生成标题 ===")
    try:
        title_response = requests.post(f"{base_url}/generate-title", json={
            "genre": workflow_data["genre"],
            "theme": workflow_data["theme"]
        })
        
        if title_response.status_code == 200:
            title_data = title_response.json()
            workflow_data["title"] = title_data["title"]
            print(f"✅ 标题生成成功: {workflow_data['title']}")
        else:
            print(f"❌ 标题生成失败: {title_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 标题生成错误: {e}")
        return
    
    print("\n=== 步骤2: 生成简洁大纲 ===")
    try:
        outline_response = requests.post(f"{base_url}/generate-outline", json={
            "genre": workflow_data["genre"],
            "theme": workflow_data["theme"],
            "title": workflow_data["title"]
        })
        
        if outline_response.status_code == 200:
            outline_data = outline_response.json()
            workflow_data["outline"] = outline_data["outline"]
            print(f"✅ 大纲生成成功")
            print(f"大纲长度: {len(workflow_data['outline'])} 字符")
            print(f"大纲预览:\n{workflow_data['outline'][:200]}...")
            
            # 验证是否为简洁版
            if len(workflow_data['outline']) < 500:
                print("✅ 大纲符合简洁要求")
            else:
                print("⚠️ 大纲可能过于详细")
        else:
            print(f"❌ 大纲生成失败: {outline_response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 大纲生成错误: {e}")
        return
    
    print("\n=== 步骤3: 测试章节生成（支持章节选择）===")
    
    # 测试生成第1章
    test_chapters = [1, 3, 5]
    
    for chapter_num in test_chapters:
        print(f"\n--- 测试生成第{chapter_num}章 ---")
        try:
            chapter_response = requests.post(f"{base_url}/generate-chapter", json={
                "title": workflow_data["title"],
                "outline": workflow_data["outline"],
                "chapter_number": chapter_num
            })
            
            if chapter_response.status_code == 200:
                chapter_data = chapter_response.json()
                chapter_content = chapter_data["content"]
                print(f"✅ 第{chapter_num}章生成成功")
                print(f"章节长度: {len(chapter_content)} 字符")
                print(f"章节预览: {chapter_content[:100]}...")
            else:
                print(f"❌ 第{chapter_num}章生成失败: {chapter_response.status_code}")
                
        except Exception as e:
            print(f"❌ 第{chapter_num}章生成错误: {e}")
    
    print("\n=== 工作流程测试完成 ===")
    print("数据联动检查:")
    print(f"- 类型: {workflow_data.get('genre', 'N/A')}")
    print(f"- 主题: {workflow_data.get('theme', 'N/A')}")
    print(f"- 标题: {workflow_data.get('title', 'N/A')}")
    print(f"- 大纲长度: {len(workflow_data.get('outline', ''))} 字符")
    
    if all(key in workflow_data for key in ['genre', 'theme', 'title', 'outline']):
        print("✅ 数据联动正常")
    else:
        print("❌ 数据联动存在问题")

if __name__ == "__main__":
    test_create_workflow()