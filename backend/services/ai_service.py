# co-novel - AI服务
import os
from openai import OpenAI
from typing import Iterator
import random

# 确保环境变量已加载
from dotenv import load_dotenv
load_dotenv()

# 初始化OpenAI客户端
try:
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
except:
    client = None
    print("Warning: OpenAI client initialization failed, using fallback mode")

class AIService:
    """AI服务类，用于与OpenAI API交互"""
    
    def __init__(self):
        self.client = client
    
    def generate_novel_content(self, prompt: str, max_tokens: int = 500) -> str:
        """
        生成小说内容
        
        Args:
            prompt: 生成内容的提示词
            max_tokens: 最大生成token数
            
        Returns:
            生成的小说内容
        """
        if self.client is None:
            return "抱歉，AI服务暂时不可用，请检查配置。"
            
        try:
            # 使用Chat API更加稳定
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "你是一个擅长创作小说的AI助手。请根据用户的要求生成高质量的小说内容。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            content = response.choices[0].message.content
            return content.strip() if content else "抱歉，AI生成内容为空。"
        except Exception as e:
            print(f"AI生成错误: {e}")
            return "抱歉，AI生成内容时出现错误。"
    
    def generate_novel_content_stream(self, prompt: str, max_tokens: int = 500) -> Iterator[str]:
        """
        流式生成小说内容
        
        Args:
            prompt: 生成内容的提示词
            max_tokens: 最大生成token数
            
        Yields:
            生成的小说内容片段
        """
        if self.client is None:
            yield "抱歉，AI服务暂时不可用，请检查配置。"
            return
            
        try:
            # 使用Chat API的流式模式
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "你是一个擅长创作小说的AI助手。请根据用户的要求生成高质量的小说内容。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                stream=True  # 启用流式响应
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"AI流式生成错误: {e}")
            yield "抱歉，AI流式生成内容时出现错误。"
    
    def generate_novel_title(self, genre: str, theme: str) -> str:
        """
        生成小说标题
        
        Args:
            genre: 小说类型
            theme: 小说主题
            
        Returns:
            生成的小说标题
        """
        print(f"正在为{genre}类型、主题'{theme}'生成标题...")
        
        # 智能标题生成逻辑，根据主题生成合适的标题
        if "最弱" in theme and "最强" in theme:
            titles_pool = [
                "《弱者逆天》",
                "《逆袭称尊》", 
                "《弱者为王》",
                "《逆天战神》",
                "《底层逆袭》",
                "《绝世逆袭》",
                "《弱者称雄》",
                "《逆天传说》",
                "《蚁族崛起》",
                "《废柴逆袭》"
            ]
            result = random.choice(titles_pool)
        elif "修炼" in theme or "修仙" in theme:
            titles_pool = [
                "《逆天修神》",
                "《仙路逆袭》",
                "《修真狂潮》",
                "《逆天仙尊》"
            ]
            result = random.choice(titles_pool)
        elif "重生" in theme:
            titles_pool = [
                "《重生称尊》",
                "《逆天重生》",
                "《重生战神》"
            ]
            result = random.choice(titles_pool)
        else:
            # 通用玄幻标题
            titles_pool = [
                f"《{genre}传奇》",
                f"《{genre}战神》", 
                f"《{genre}至尊》",
                f"《{genre}霸主》"
            ]
            result = random.choice(titles_pool)
        
        print(f"生成的标题: {result}")
        return result
    
    def generate_novel_outline(self, genre: str, theme: str, title: str) -> str:
        """
        生成小说大纲
        
        Args:
            genre: 小说类型
            theme: 小说主题
            title: 小说标题
            
        Returns:
            生成的小说大纲
        """
        try:
            prompt = f"""请为以下小说生成简洁的章节大纲：

标题：{title}
类型：{genre}
主题：{theme}

要求：
1. 生成5-8章的简洁大纲
2. 每章只需章节标题和一句话概括
3. 情节要连贯，逻辑合理
4. 符合{genre}类型的特点
5. 围绕{theme}这个主题展开
6. 每章概括控制在30字以内

请用以下格式输出：
第一章：[章节标题]
[一句话概括，30字以内]

第二章：[章节标题]
[一句话概括，30字以内]

..."""
            return self.generate_novel_content(prompt, 400)
        except Exception as e:
            # 提供fallback大纲
            fallback_outline = f"""第一章：初入{genre}世界
主角意外发现自己的特殊能力，开始{theme}的旅程。

第二章：初试身手
主角遇到挑战，凭借智慧和勇气取得意想不到的胜利。

第三章：奇遇获宝
主角获得珍贵的宝物或传承，实力开始提升。

第四章：强敌来袭
主角遇到强大敌人，体现"{theme}"的核心精神。

第五章：绝地反击
主角在绝境中爆发潜力，完成不可能的逆转。"""
            return fallback_outline
    
    def generate_novel_outline_stream(self, genre: str, theme: str, title: str) -> Iterator[str]:
        """
        流式生成小说大纲
        
        Args:
            genre: 小说类型
            theme: 小说主题
            title: 小说标题
            
        Yields:
            生成的小说大纲片段
        """
        prompt = f"""请为以下小说生成简洁的章节大纲：

标题：{title}
类型：{genre}
主题：{theme}

要求：
1. 生成5-8章的简洁大纲
2. 每章只需章节标题和一句话概括
3. 情节要连贯，逻辑合理
4. 符合{genre}类型的特点
5. 围绕{theme}这个主题展开
6. 每章概括控制在30字以内

请用以下格式输出：
第一章：[章节标题]
[一句话概括，30字以内]

第二章：[章节标题]
[一句话概括，30字以内]

..."""
        
        if self.client is None:
            # 使用fallback大纲，逐字符返回
            fallback_outline = f"""第一章：初入{genre}世界
主角意外发现自己的特殊能力，开始{theme}的旅程。

第二章：初试身手
主角遇到挑战，凭借智慧和勇气取得意想不到的胜利。

第三章：奇遇获宝
主角获得珍贵的宝物或传承，实力开始提升。

第四章：强敌来袭
主角遇到强大敌人，体现"{theme}"的核心精神。

第五章：绝地反击
主角在绝境中爆发潜力，完成不可能的逆转。"""
            
            # 逐字符返回
            import time
            for char in fallback_outline:
                yield char
                time.sleep(0.01)  # 模拟流式效果
            return
            
        try:
            # 使用Chat API的流式模式
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "你是一个擅长创作小说的AI助手。请根据用户的要求生成高质量的小说大纲。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.7,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"AI流式生成大纲错误: {e}")
            # 使用fallback大纲，逐字符返回
            fallback_outline = f"""第一章：初入{genre}世界
主角意外发现自己的特殊能力，开始{theme}的旅程。

第二章：初试身手
主角遇到挑战，凭借智慧和勇气取得意想不到的胜利。

第三章：奇遇获宝
主角获得珍贵的宝物或传承，实力开始提升。

第四章：强敌来袭
主角遇到强大敌人，体现"{theme}"的核心精神。

第五章：绝地反击
主角在绝境中爆发潜力，完成不可能的逆转。"""
            
            # 逐字符返回
            import time
            for char in fallback_outline:
                yield char
                time.sleep(0.01)  # 模拟流式效果
    
    def generate_chapter_content(self, title: str, outline: str, chapter_number: int = 1) -> str:
        """
        根据大纲生成指定章节的内容
        
        Args:
            title: 小说标题
            outline: 小说大纲
            chapter_number: 章节号
            
        Returns:
            生成的章节内容
        """
        prompt = f"""请根据以下信息写第{chapter_number}章的完整内容：

小说标题：{title}

完整大纲：
{outline}

要求：
1. 写出第{chapter_number}章的完整内容，约1000-1500字
2. 内容要生动有趣，有对话和场景描写
3. 严格按照大纲中第{chapter_number}章的情节发展
4. 文笔流畅，符合现代小说的写作风格
5. 如果是第一章，要有引人入胜的开头

请直接输出章节内容，不需要额外的说明："""
        return self.generate_novel_content(prompt, 1200)
    
    def generate_chapter_content_stream(self, title: str, outline: str, chapter_number: int = 1) -> Iterator[str]:
        """
        流式生成章节内容
        
        Args:
            title: 小说标题
            outline: 小说大纲
            chapter_number: 章节号
            
        Yields:
            生成的章节内容片段
        """
        prompt = f"""请根据以下信息写第{chapter_number}章的完整内容：

小说标题：{title}

完整大纲：
{outline}

要求：
1. 写出第{chapter_number}章的完整内容，约1000-1500字
2. 内容要生动有趣，有对话和场景描写
3. 严格按照大纲中第{chapter_number}章的情节发展
4. 文笔流畅，符合现代小说的写作风格
5. 如果是第一章，要有引人入胜的开头

请直接输出章节内容，不需要额外的说明："""
        
        if self.client is None:
            yield "抱歉，AI服务暂时不可用，请检查配置。"
            return
            
        try:
            # 使用Chat API的流式模式
            response = self.client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                messages=[
                    {"role": "system", "content": "你是一个擅长创作小说的AI助手。请根据用户的要求生成高质量的小说内容。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1200,
                temperature=0.7,
                stream=True
            )
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            print(f"AI流式生成章节内容错误: {e}")
            yield "抱歉，AI流式生成章节内容时出现错误。"

    def get_ai_suggestions(self, current_content: str, suggestion_type: str) -> str:
        """
        获取AI建议
        
        Args:
            current_content: 当前内容
            suggestion_type: 建议类型（如：续写、修改、扩展等）
            
        Returns:
            AI建议内容
        """
        prompt = f"基于以下内容，{suggestion_type}：\n\n{current_content}"
        return self.generate_novel_content(prompt, 300)