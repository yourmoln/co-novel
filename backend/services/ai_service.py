# co-novel - AI服务
import os
from openai import OpenAI

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

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
        try:
            response = self.client.completions.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"AI生成错误: {e}")
            return "抱歉，AI生成内容时出现错误。"
    
    def generate_novel_title(self, genre: str, theme: str) -> str:
        """
        生成小说标题
        
        Args:
            genre: 小说类型
            theme: 小说主题
            
        Returns:
            生成的小说标题
        """
        prompt = f"为一个{genre}类型的小说，主题是{theme}，生成一个吸引人的标题。"
        return self.generate_novel_content(prompt, 100)
    
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
