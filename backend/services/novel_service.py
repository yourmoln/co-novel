# co-novel - 业务服务层
from typing import Optional, List, Dict, Any
from datetime import datetime

from models.novel import (
    NovelProject, Chapter, CreationSession, 
    NovelGenre, NovelStatus, ChapterStatus, CreationStep,
    TitleGenerationRequest, OutlineGenerationRequest, ChapterGenerationRequest,
    APIResponse
)
from services.data_service import data_manager
from services.ai_service import AIService


class NovelBusinessService:
    """小说创作业务服务"""
    
    def __init__(self):
        self.ai_service = AIService()
    
    def create_novel_project(self, genre: NovelGenre, theme: str) -> APIResponse:
        """创建新的小说项目"""
        try:
            # 创建小说项目
            novel = data_manager.create_novel(genre, theme)
            
            # 创建关联的创作会话
            session = data_manager.create_session(novel.id)
            
            return APIResponse(
                success=True,
                message="小说项目创建成功",
                data={
                    "novel": novel.dict(),
                    "session": session.dict()
                }
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"创建小说项目失败: {str(e)}",
                error_code="CREATE_PROJECT_FAILED"
            )
    
    def generate_titles(self, request: TitleGenerationRequest) -> APIResponse:
        """生成小说标题"""
        try:
            # 生成多个标题选项
            titles = self.ai_service.generate_multiple_titles(
                request.genre.value, 
                request.theme, 
                request.count
            )
            
            return APIResponse(
                success=True,
                message="标题生成成功",
                data={"titles": titles}
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"标题生成失败: {str(e)}",
                error_code="TITLE_GENERATION_FAILED"
            )
    
    def generate_outline(self, request: OutlineGenerationRequest) -> APIResponse:
        """生成小说大纲"""
        try:
            outline = self.ai_service.generate_novel_outline(
                request.genre.value,
                request.theme,
                request.title
            )
            
            return APIResponse(
                success=True,
                message="大纲生成成功",
                data={"outline": outline}
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"大纲生成失败: {str(e)}",
                error_code="OUTLINE_GENERATION_FAILED"
            )
    
    def generate_chapter(self, request: ChapterGenerationRequest) -> APIResponse:
        """生成章节内容"""
        try:
            content = self.ai_service.generate_chapter_content(
                request.title,
                request.outline,
                request.chapter_number,
                request.custom_title
            )
            
            return APIResponse(
                success=True,
                message="章节生成成功",
                data={
                    "content": content,
                    "chapter_number": request.chapter_number,
                    "chapter_title": request.custom_title or f"第{request.chapter_number}章"
                }
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"章节生成失败: {str(e)}",
                error_code="CHAPTER_GENERATION_FAILED"
            )
    
    def save_novel_content(self, novel_id: str, title: str, outline: str) -> APIResponse:
        """保存小说基础内容"""
        try:
            novel = data_manager.get_novel(novel_id)
            if not novel:
                return APIResponse(
                    success=False,
                    message="小说项目不存在",
                    error_code="NOVEL_NOT_FOUND"
                )
            
            # 更新小说信息
            novel.title = title
            novel.outline = outline
            novel.status = NovelStatus.IN_PROGRESS
            
            # 如果是第一次设置标题，加入到生成标题列表
            if title not in novel.generated_titles:
                novel.generated_titles.append(title)
            
            success = data_manager.update_novel(novel)
            
            if success:
                return APIResponse(
                    success=True,
                    message="小说内容保存成功",
                    data=novel.dict()
                )
            else:
                return APIResponse(
                    success=False,
                    message="保存失败",
                    error_code="SAVE_FAILED"
                )
                
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"保存小说内容失败: {str(e)}",
                error_code="SAVE_CONTENT_FAILED"
            )
    
    def save_chapter(self, novel_id: str, chapter_number: int, content: str, title: Optional[str] = None) -> APIResponse:
        """保存章节内容"""
        try:
            # 检查小说是否存在
            novel = data_manager.get_novel(novel_id)
            if not novel:
                return APIResponse(
                    success=False,
                    message="小说项目不存在",
                    error_code="NOVEL_NOT_FOUND"
                )
            
            # 查找是否已有该章节
            existing_chapters = data_manager.get_chapters_by_novel(novel_id)
            existing_chapter = None
            for ch in existing_chapters:
                if ch.chapter_number == chapter_number:
                    existing_chapter = ch
                    break
            
            if existing_chapter:
                # 更新现有章节
                existing_chapter.content = content
                existing_chapter.title = title or existing_chapter.title
                existing_chapter.status = ChapterStatus.COMPLETED
                existing_chapter.generated_by_ai = True
                existing_chapter.ai_model_used = self.ai_service.model
                success = data_manager.update_chapter(existing_chapter)
                chapter = existing_chapter
            else:
                # 创建新章节
                chapter = data_manager.create_chapter(novel_id, chapter_number, title)
                chapter.content = content
                chapter.status = ChapterStatus.COMPLETED
                chapter.generated_by_ai = True
                chapter.ai_model_used = self.ai_service.model
                success = data_manager.update_chapter(chapter)
            
            if success:
                # 更新小说统计信息
                novel.chapter_count = len(data_manager.get_chapters_by_novel(novel_id))
                novel.total_word_count = sum(ch.word_count for ch in data_manager.get_chapters_by_novel(novel_id))
                data_manager.update_novel(novel)
                
                return APIResponse(
                    success=True,
                    message="章节保存成功",
                    data=chapter.dict()
                )
            else:
                return APIResponse(
                    success=False,
                    message="章节保存失败",
                    error_code="CHAPTER_SAVE_FAILED"
                )
                
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"保存章节失败: {str(e)}",
                error_code="SAVE_CHAPTER_FAILED"
            )
    
    def get_novel_details(self, novel_id: str) -> APIResponse:
        """获取小说详细信息"""
        try:
            novel = data_manager.get_novel(novel_id)
            if not novel:
                return APIResponse(
                    success=False,
                    message="小说项目不存在",
                    error_code="NOVEL_NOT_FOUND"
                )
            
            chapters = data_manager.get_chapters_by_novel(novel_id)
            session = data_manager.get_active_session(novel_id)
            
            return APIResponse(
                success=True,
                message="获取小说详情成功",
                data={
                    "novel": novel.dict(),
                    "chapters": [ch.dict() for ch in chapters],
                    "session": session.dict() if session else None
                }
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"获取小说详情失败: {str(e)}",
                error_code="GET_NOVEL_FAILED"
            )
    
    def list_novels(self, limit: int = 20) -> APIResponse:
        """列出小说项目"""
        try:
            novels = data_manager.list_novels(limit)
            return APIResponse(
                success=True,
                message="获取小说列表成功",
                data={
                    "novels": [novel.dict() for novel in novels],
                    "total": len(novels)
                }
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"获取小说列表失败: {str(e)}",
                error_code="LIST_NOVELS_FAILED"
            )
    
    def update_session_step(self, session_id: str, action: str, data: Optional[Dict[str, Any]] = None) -> APIResponse:
        """更新创作会话步骤"""
        try:
            session = data_manager.get_session(session_id)
            if not session:
                return APIResponse(
                    success=False,
                    message="创作会话不存在",
                    error_code="SESSION_NOT_FOUND"
                )
            
            if action == "next":
                session.next_step()
            elif action == "prev":
                session.prev_step()
            elif action == "update" and data:
                for key, value in data.items():
                    session.update_session_data(key, value)
            elif action == "save":
                session.update_activity()
            
            success = data_manager.update_session(session)
            
            if success:
                return APIResponse(
                    success=True,
                    message="会话更新成功",
                    data=session.dict()
                )
            else:
                return APIResponse(
                    success=False,
                    message="会话更新失败",
                    error_code="SESSION_UPDATE_FAILED"
                )
                
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"更新会话失败: {str(e)}",
                error_code="UPDATE_SESSION_FAILED"
            )
    
    def get_statistics(self) -> APIResponse:
        """获取系统统计信息"""
        try:
            stats = data_manager.get_statistics()
            return APIResponse(
                success=True,
                message="获取统计信息成功",
                data=stats
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"获取统计信息失败: {str(e)}",
                error_code="GET_STATISTICS_FAILED"
            )
    
    def save_chapter_new(self, title: str, content: str, chapter_number: int, 
                         custom_title: Optional[str] = None, genre: Optional[str] = None, 
                         theme: Optional[str] = None, outline: Optional[str] = None) -> Dict[str, Any]:
        """保存章节内容新接口"""
        try:
            # 查找或创建小说项目
            novels = data_manager.list_novels()
            existing_novel = None
            
            # 查找匹配的小说项目
            for novel in novels:
                if novel.title == title and novel.theme == theme:
                    existing_novel = novel
                    break
            
            if not existing_novel:
                # 创建新的小说项目
                from models.novel import NovelGenre
                try:
                    genre_enum = NovelGenre(genre)
                except ValueError:
                    genre_enum = NovelGenre.FANTASY  # 默认类型
                
                existing_novel = data_manager.create_novel(genre_enum, theme or '默认主题')
                existing_novel.title = title
                existing_novel.outline = outline
                data_manager.update_novel(existing_novel)
            
            # 保存章节
            chapter = data_manager.create_chapter(
                existing_novel.id, 
                chapter_number, 
                custom_title or f"第{chapter_number}章"
            )
            chapter.content = content
            chapter.status = ChapterStatus.COMPLETED
            chapter.generated_by_ai = True
            chapter.ai_model_used = getattr(self.ai_service, 'model', 'gpt-3.5-turbo')
            
            success = data_manager.update_chapter(chapter)
            
            if success:
                # 更新小说统计信息
                chapters = data_manager.get_chapters_by_novel(existing_novel.id)
                existing_novel.chapter_count = len(chapters)
                existing_novel.total_word_count = sum(ch.word_count for ch in chapters)
                data_manager.update_novel(existing_novel)
                
                return {
                    "success": True,
                    "message": "章节保存成功",
                    "chapter_id": chapter.id,
                    "novel_id": existing_novel.id
                }
            else:
                return {
                    "success": False,
                    "message": "章节保存失败",
                    "chapter_id": None,
                    "novel_id": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"保存章节失败: {str(e)}",
                "chapter_id": None,
                "novel_id": None
            }
    
    def get_all_saved_chapters(self) -> List[Dict[str, Any]]:
        """获取所有已保存的章节列表"""
        try:
            novels = data_manager.list_novels()
            all_chapters = []
            
            for novel in novels:
                chapters = data_manager.get_chapters_by_novel(novel.id)
                for chapter in chapters:
                    chapter_info = {
                        "chapter_id": chapter.id,
                        "novel_id": novel.id,
                        "title": chapter.title,
                        "chapter_number": chapter.chapter_number,
                        "word_count": chapter.word_count,
                        "created_at": chapter.created_at.isoformat() if isinstance(chapter.created_at, datetime) else chapter.created_at,
                        "novel_title": novel.title or f"{novel.genre}小说",
                        "genre": novel.genre.value if hasattr(novel.genre, 'value') else str(novel.genre),
                        "theme": novel.theme
                    }
                    all_chapters.append(chapter_info)
            
            # 按创建时间倒序排列
            all_chapters.sort(key=lambda x: x["created_at"], reverse=True)
            return all_chapters
            
        except Exception as e:
            print(f"获取章节列表失败: {str(e)}")
            return []
    
    def get_chapter_content(self, chapter_id: str) -> Optional[Dict[str, Any]]:
        """获取特定章节的完整内容"""
        try:
            chapter = data_manager.get_chapter(chapter_id)
            if not chapter:
                return None
            
            # 获取小说信息
            novel = data_manager.get_novel(chapter.novel_id)
            if not novel:
                return None
            
            return {
                "chapter_id": chapter.id,
                "novel_id": novel.id,
                "title": chapter.title,
                "content": chapter.content,
                "chapter_number": chapter.chapter_number,
                "word_count": chapter.word_count,
                "created_at": chapter.created_at.isoformat() if isinstance(chapter.created_at, datetime) else chapter.created_at,
                "updated_at": chapter.updated_at.isoformat() if isinstance(chapter.updated_at, datetime) else chapter.updated_at,
                "novel_title": novel.title or f"{novel.genre}小说",
                "genre": novel.genre.value if hasattr(novel.genre, 'value') else str(novel.genre),
                "theme": novel.theme,
                "outline": novel.outline
            }
            
        except Exception as e:
            print(f"获取章节内容失败: {str(e)}")
            return None
    
    def update_chapter_position(self, chapter_id: str, new_position: int) -> bool:
        """更新章节位置"""
        try:
            chapter = data_manager.get_chapter(chapter_id)
            if not chapter:
                return False
            
            # 检查新位置是否合理
            if new_position < 1 or new_position > 99:
                return False
            
            # 检查是否已有相同位置的章节
            existing_chapters = data_manager.get_chapters_by_novel(chapter.novel_id)
            for existing_chapter in existing_chapters:
                if (existing_chapter.id != chapter_id and 
                    existing_chapter.chapter_number == new_position):
                    # 如果有冲突，可以选择交换位置或拒绝
                    # 这里选择简单的拒绝处理
                    print(f"第{new_position}章已存在，位置更新失败")
                    return False
            
            # 更新章节位置
            chapter.chapter_number = new_position
            chapter.updated_at = datetime.now()
            
            # 如果没有自定义标题，同时更新标题
            if not chapter.title or chapter.title == f"第{chapter.chapter_number}章":
                chapter.title = f"第{new_position}章"
            
            return data_manager.update_chapter(chapter)
            
        except Exception as e:
            print(f"更新章节位置失败: {str(e)}")
            return False
    
    def cleanup_resources(self) -> APIResponse:
        """清理资源"""
        try:
            # 清理过期缓存
            deleted_cache = data_manager.cleanup_old_cache(days=7)
            
            return APIResponse(
                success=True,
                message="资源清理完成",
                data={"deleted_cache_entries": deleted_cache}
            )
        except Exception as e:
            return APIResponse(
                success=False,
                message=f"资源清理失败: {str(e)}",
                error_code="CLEANUP_FAILED"
            )


# 全局业务服务实例
novel_service = NovelBusinessService()