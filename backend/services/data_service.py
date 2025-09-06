# co-novel - 数据管理服务
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

from models.novel import (
    NovelProject, Chapter, CreationSession, AIGenerationCache,
    NovelGenre, NovelStatus, ChapterStatus, CreationStep
)


class DataManager:
    """数据管理器 - 使用文件存储模拟数据库操作"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # 各类数据的存储文件
        self.novels_file = self.data_dir / "novels.json"
        self.chapters_file = self.data_dir / "chapters.json"
        self.sessions_file = self.data_dir / "sessions.json"
        self.cache_file = self.data_dir / "ai_cache.json"
        
        # 初始化数据文件
        self._init_data_files()
    
    def _init_data_files(self):
        """初始化数据文件"""
        for file_path in [self.novels_file, self.chapters_file, self.sessions_file, self.cache_file]:
            if not file_path.exists():
                file_path.write_text("[]", encoding="utf-8")
    
    def _load_data(self, file_path: Path) -> List[Dict]:
        """加载数据"""
        try:
            content = file_path.read_text(encoding="utf-8")
            return json.loads(content)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_data(self, file_path: Path, data: List[Dict]):
        """保存数据"""
        # 处理日期时间序列化
        def json_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
        
        file_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2, default=json_serializer), 
            encoding="utf-8"
        )
    
    # === 小说项目管理 ===
    
    def create_novel(self, genre: NovelGenre, theme: str) -> NovelProject:
        """创建新小说项目"""
        novel = NovelProject(genre=genre, theme=theme)
        
        novels = self._load_data(self.novels_file)
        novels.append(novel.dict())
        self._save_data(self.novels_file, novels)
        
        return novel
    
    def get_novel(self, novel_id: str) -> Optional[NovelProject]:
        """获取小说项目"""
        novels = self._load_data(self.novels_file)
        for novel_data in novels:
            if novel_data["id"] == novel_id:
                return NovelProject(**novel_data)
        return None
    
    def update_novel(self, novel: NovelProject) -> bool:
        """更新小说项目"""
        novels = self._load_data(self.novels_file)
        for i, novel_data in enumerate(novels):
            if novel_data["id"] == novel.id:
                novel.update_timestamp()
                novels[i] = novel.dict()
                self._save_data(self.novels_file, novels)
                return True
        return False
    
    def list_novels(self, limit: int = 20) -> List[NovelProject]:
        """列出小说项目"""
        novels = self._load_data(self.novels_file)
        # 按更新时间倒序排列
        novels.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return [NovelProject(**novel_data) for novel_data in novels[:limit]]
    
    def delete_novel(self, novel_id: str) -> bool:
        """删除小说项目"""
        novels = self._load_data(self.novels_file)
        original_count = len(novels)
        novels = [n for n in novels if n["id"] != novel_id]
        
        if len(novels) < original_count:
            self._save_data(self.novels_file, novels)
            # 同时删除相关章节
            self.delete_chapters_by_novel(novel_id)
            return True
        return False
    
    # === 章节管理 ===
    
    def create_chapter(self, novel_id: str, chapter_number: int, title: Optional[str] = None) -> Chapter:
        """创建新章节"""
        chapter = Chapter(
            novel_id=novel_id,
            chapter_number=chapter_number,
            title=title or f"第{chapter_number}章"
        )
        
        chapters = self._load_data(self.chapters_file)
        chapters.append(chapter.dict())
        self._save_data(self.chapters_file, chapters)
        
        return chapter
    
    def get_chapter(self, chapter_id: str) -> Optional[Chapter]:
        """获取章节"""
        chapters = self._load_data(self.chapters_file)
        for chapter_data in chapters:
            if chapter_data["id"] == chapter_id:
                return Chapter(**chapter_data)
        return None
    
    def get_chapters_by_novel(self, novel_id: str) -> List[Chapter]:
        """获取小说的所有章节"""
        chapters = self._load_data(self.chapters_file)
        novel_chapters = [Chapter(**ch) for ch in chapters if ch["novel_id"] == novel_id]
        # 按章节号排序
        novel_chapters.sort(key=lambda x: x.chapter_number)
        return novel_chapters
    
    def update_chapter(self, chapter: Chapter) -> bool:
        """更新章节"""
        chapters = self._load_data(self.chapters_file)
        for i, chapter_data in enumerate(chapters):
            if chapter_data["id"] == chapter.id:
                chapter.update_word_count()
                chapters[i] = chapter.dict()
                self._save_data(self.chapters_file, chapters)
                return True
        return False
    
    def delete_chapters_by_novel(self, novel_id: str) -> int:
        """删除小说的所有章节"""
        chapters = self._load_data(self.chapters_file)
        original_count = len(chapters)
        chapters = [ch for ch in chapters if ch["novel_id"] != novel_id]
        
        deleted_count = original_count - len(chapters)
        if deleted_count > 0:
            self._save_data(self.chapters_file, chapters)
        return deleted_count
    
    # === 创作会话管理 ===
    
    def create_session(self, novel_id: str) -> CreationSession:
        """创建创作会话"""
        session = CreationSession(novel_id=novel_id)
        
        sessions = self._load_data(self.sessions_file)
        sessions.append(session.dict())
        self._save_data(self.sessions_file, sessions)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[CreationSession]:
        """获取创作会话"""
        sessions = self._load_data(self.sessions_file)
        for session_data in sessions:
            if session_data["id"] == session_id:
                return CreationSession(**session_data)
        return None
    
    def get_active_session(self, novel_id: str) -> Optional[CreationSession]:
        """获取活跃的创作会话"""
        sessions = self._load_data(self.sessions_file)
        for session_data in sessions:
            if (session_data["novel_id"] == novel_id and 
                session_data.get("is_active", True)):
                return CreationSession(**session_data)
        return None
    
    def update_session(self, session: CreationSession) -> bool:
        """更新创作会话"""
        sessions = self._load_data(self.sessions_file)
        for i, session_data in enumerate(sessions):
            if session_data["id"] == session.id:
                sessions[i] = session.dict()
                self._save_data(self.sessions_file, sessions)
                return True
        return False
    
    def deactivate_session(self, session_id: str) -> bool:
        """停用创作会话"""
        sessions = self._load_data(self.sessions_file)
        for i, session_data in enumerate(sessions):
            if session_data["id"] == session_id:
                sessions[i]["is_active"] = False
                sessions[i]["updated_at"] = datetime.now().isoformat()
                self._save_data(self.sessions_file, sessions)
                return True
        return False
    
    # === AI缓存管理 ===
    
    def get_cache(self, cache_key: str) -> Optional[AIGenerationCache]:
        """获取缓存内容"""
        caches = self._load_data(self.cache_file)
        for cache_data in caches:
            if cache_data["cache_key"] == cache_key:
                cache = AIGenerationCache(**cache_data)
                cache.increment_hit()
                self.update_cache(cache)
                return cache
        return None
    
    def save_cache(self, cache_key: str, content_type: str, content: str, **metadata) -> AIGenerationCache:
        """保存缓存内容"""
        cache = AIGenerationCache(
            cache_key=cache_key,
            content_type=content_type,
            generated_content=content,
            **metadata
        )
        
        caches = self._load_data(self.cache_file)
        caches.append(cache.dict())
        self._save_data(self.cache_file, caches)
        
        return cache
    
    def update_cache(self, cache: AIGenerationCache) -> bool:
        """更新缓存"""
        caches = self._load_data(self.cache_file)
        for i, cache_data in enumerate(caches):
            if cache_data["id"] == cache.id:
                caches[i] = cache.dict()
                self._save_data(self.cache_file, caches)
                return True
        return False
    
    def cleanup_old_cache(self, days: int = 30) -> int:
        """清理过期缓存"""
        caches = self._load_data(self.cache_file)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        original_count = len(caches)
        caches = [
            cache for cache in caches
            if datetime.fromisoformat(cache["created_at"]) > cutoff_date
        ]
        
        deleted_count = original_count - len(caches)
        if deleted_count > 0:
            self._save_data(self.cache_file, caches)
        
        return deleted_count
    
    # === 统计信息 ===
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取统计信息"""
        novels = self._load_data(self.novels_file)
        chapters = self._load_data(self.chapters_file)
        sessions = self._load_data(self.sessions_file)
        caches = self._load_data(self.cache_file)
        
        # 计算总字数
        total_words = sum(ch.get("word_count", 0) for ch in chapters)
        
        # 按类型统计小说数量
        genre_stats = {}
        for novel in novels:
            genre = novel.get("genre", "未知")
            genre_stats[genre] = genre_stats.get(genre, 0) + 1
        
        # 活跃会话数
        active_sessions = sum(1 for s in sessions if s.get("is_active", True))
        
        # 缓存命中率（简化计算）
        cache_hits = sum(c.get("hit_count", 1) for c in caches)
        cache_efficiency = cache_hits / len(caches) if caches else 0
        
        return {
            "total_novels": len(novels),
            "total_chapters": len(chapters),
            "total_words": total_words,
            "active_sessions": active_sessions,
            "cache_entries": len(caches),
            "cache_efficiency": round(cache_efficiency, 2),
            "genre_distribution": genre_stats,
            "last_updated": datetime.now().isoformat()
        }


# 全局数据管理器实例
data_manager = DataManager()