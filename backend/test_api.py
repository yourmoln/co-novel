#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试大纲生成API
"""

import requests
import json

def test_outline_api():
    print("测试大纲生成API...")
    
    # API基础URL
    base_url = "http://localhost:8000/api/ai"
    
    # 测试数据
    test_data = {
        "genre": "玄幻",
        "theme": "以最弱战最强", 
        "title": "《逆天传说》"
    }
    
    try:
        # 测试普通大纲生成
        print("\n=== 测试普通大纲生成 ===")
        response = requests.post(f"{base_url}/generate-outline", json=test_data)
        
        if response.status_code == 200:
            result = response.json()
            outline = result['outline']
            print(f"生成成功！")
            print(f"大纲内容:\n{outline}")
            print(f"大纲字符数: {len(outline)}")
            
            # 检查是否为简洁版本
            if len(outline) < 500:
                print("✅ 大纲长度合适（简洁版）")
            else:
                print("❌ 大纲可能仍然过于详细")
                
            # 检查是否包含"第一章"等关键词
            if "第一章" in outline and "第二章" in outline:
                print("✅ 大纲格式正确")
            else:
                print("❌ 大纲格式可能有问题")
                
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
        # 测试流式大纲生成
        print("\n=== 测试流式大纲生成 ===")
        response = requests.post(f"{base_url}/generate-outline-stream", json=test_data, stream=True)
        
        if response.status_code == 200:
            print("✅ 流式API响应成功")
            print("前几行流式内容:")
            
            content_lines = []
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    if line_str.startswith('data: '):
                        try:
                            data_json = json.loads(line_str[6:])
                            if 'choices' in data_json and len(data_json['choices']) > 0:
                                delta = data_json['choices'][0].get('delta', {})
                                if 'content' in delta and delta['content']:
                                    content_lines.append(delta['content'])
                                    print(delta['content'], end='', flush=True)
                                    
                                    # 只显示前几行作为示例
                                    if len(''.join(content_lines)) > 100:
                                        print("\n... (流式传输正常)")
                                        break
                        except:
                            pass
        else:
            print(f"❌ 流式API请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")

if __name__ == "__main__":
    test_outline_api()