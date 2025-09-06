# co-novel - 小说数据模型
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import uuid
import hashlib


class NovelGenre(str, Enum):
    """小说类型枚举"""
    FANTASY = "玄幻"
    URBAN = "都市"
    SCIFI = "科幻"
    WUXIA = "武侠"
    ROMANCE = "言情"


class NovelStatus(str, Enum):
    """小说状态枚举"""
    DRAFT = "草稿"
    IN_PROGRESS = "创作中"
    COMPLETED = "已完成"
    PUBLISHED = "已发布"


class ChapterStatus(str, Enum):
    """章节状态枚举"""
    DRAFT = "草稿"
    GENERATING = "生成中"
    COMPLETED = "已完成"
    REVIEWED = "已审阅"


class CreationStep(int, Enum):
    """创作步骤枚举"""
    BASIC_SETUP = 0      # 基础设置
    TITLE_GENERATION = 1  # 标题生成
    OUTLINE_CREATION = 2  # 大纲创建
    CONTENT_REVIEW = 3    # 内容确认
    CHAPTER_GENERATION = 4  # 章节生成


class NovelProject(BaseModel):
    """小说项目数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: Optional[str] = None
    genre: NovelGenre
    theme: str
    outline: Optional[str] = None
    status: NovelStatus = NovelStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # AI生成的候选标题
    generated_titles: List[str] = Field(default_factory=list)
    # 用户编辑过的内容
    user_edits: Dict[str, Any] = Field(default_factory=dict)
    # 总字数
    total_word_count: int = 0
    # 章节数
    chapter_count: int = 0
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def update_timestamp(self):
        """更新时间戳"""
        self.updated_at = datetime.now()


class Chapter(BaseModel):
    """章节数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    novel_id: str
    chapter_number: int
    title: Optional[str] = None
    content: Optional[str] = None
    status: ChapterStatus = ChapterStatus.DRAFT
    word_count: int = 0
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # AI生成信息
    generated_by_ai: bool = False
    ai_model_used: Optional[str] = None
    generation_prompt: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def update_word_count(self):
        """更新字数统计"""
        if self.content:
            self.word_count = len(self.content.replace(' ', '').replace('\n', ''))
        else:
            self.word_count = 0
        self.updated_at = datetime.now()


class CreationSession(BaseModel):
    """创作会话数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    novel_id: str
    current_step: CreationStep = CreationStep.BASIC_SETUP
    session_data: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    
    # 会话状态
    is_active: bool = True
    last_activity: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    def next_step(self):
        """进入下一步"""
        if self.current_step.value < 4:
            self.current_step = CreationStep(self.current_step.value + 1)
            self.update_activity()
    
    def prev_step(self):
        """返回上一步"""
        if self.current_step.value > 0:
            self.current_step = CreationStep(self.current_step.value - 1)
            self.update_activity()
    
    def update_activity(self):
        """更新活动时间"""
        self.last_activity = datetime.now()
        self.updated_at = datetime.now()
    
    def update_session_data(self, key: str, value: Any):
        """更新会话数据"""
        self.session_data[key] = value
        self.update_activity()


class AIGenerationCache(BaseModel):
    """AI生成内容缓存模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cache_key: str  # 基于输入参数生成的缓存键
    content_type: str  # title, outline, chapter等
    generated_content: str
    genre: Optional[str] = None
    theme: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    hit_count: int = 1  # 缓存命中次数
    last_hit: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @staticmethod
    def generate_cache_key(content_type: str, **kwargs) -> str:
        """生成缓存键"""
        # 将参数排序并组合成字符串
        param_str = f"{content_type}:" + ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
        # 生成MD5哈希
        return hashlib.md5(param_str.encode()).hexdigest()
    
    def increment_hit(self):
        """增加命中次数"""
        self.hit_count += 1
        self.last_hit = datetime.now()


class APIResponse(BaseModel):
    """统一API响应模型"""
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class GenerationRequest(BaseModel):
    """生成请求基础模型"""
    genre: NovelGenre
    theme: str


class TitleGenerationRequest(GenerationRequest):
    """标题生成请求"""
    count: int = Field(default=3, ge=1, le=10)  # 生成数量限制


class OutlineGenerationRequest(GenerationRequest):
    """大纲生成请求"""
    title: str
    chapter_count: int = Field(default=8, ge=3, le=20)  # 章节数量限制


class ChapterGenerationRequest(BaseModel):
    """章节生成请求"""
    title: str
    outline: str
    chapter_number: int = Field(ge=1)
    custom_title: Optional[str] = None
    word_count_target: int = Field(default=1500, ge=500, le=3000)  # 目标字数


class CreationSessionRequest(BaseModel):
    """创作会话请求"""
    session_id: Optional[str] = None
    action: str  # next, prev, update, save
    data: Optional[Dict[str, Any]] = None