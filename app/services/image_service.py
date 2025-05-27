import os
import time
from typing import Dict, List, Optional, Tuple
from fastapi import UploadFile
from datetime import datetime

from app.utils.file_utils import (
    save_upload_file, 
    delete_file, 
    list_files, 
    UPLOAD_DIR
)

class ImageService:
    @staticmethod
    async def upload_image(file: UploadFile) -> Tuple[bool, str, Optional[Dict]]:
        """
        上传图片
        
        参数:
            file: 上传的文件
            
        返回:
            Tuple[bool, str, Optional[Dict]]: (是否成功, 消息, 图片信息)
        """
        success, message, filename = await save_upload_file(file)
        
        if not success:
            return success, message, None
            
        # 获取文件信息
        file_path = os.path.join(UPLOAD_DIR, filename)
        file_size = os.path.getsize(file_path)
        
        # 创建图片信息
        image_info = {
            "id": filename.split('.')[0],  # UUID作为ID
            "filename": file.filename,
            "url": f"/static/images/{filename}",
            "size": file_size,
            "mime_type": file.content_type,
            "created_at": datetime.now().isoformat()
        }
        
        return True, "图片上传成功", image_info
    
    @staticmethod
    def get_image_list() -> List[Dict]:
        """
        获取图片列表
        
        返回:
            List[Dict]: 图片信息列表
        """
        files = list_files()
        image_list = []
        
        for filename in files:
            file_path = os.path.join(UPLOAD_DIR, filename)
            
            # 仅处理存在的文件
            if os.path.exists(file_path):
                # 获取文件基本信息
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                created_at = datetime.fromtimestamp(file_stats.st_ctime).isoformat()
                
                # 从文件名推断MIME类型
                mime_type = "image/jpeg"  # 默认
                if filename.endswith(".png"):
                    mime_type = "image/png"
                elif filename.endswith(".gif"):
                    mime_type = "image/gif"
                elif filename.endswith(".webp"):
                    mime_type = "image/webp"
                
                image_info = {
                    "id": filename.split('.')[0],  # UUID作为ID
                    "filename": filename,
                    "url": f"/static/images/{filename}",
                    "size": file_size,
                    "mime_type": mime_type,
                    "created_at": created_at
                }
                
                image_list.append(image_info)
        
        return image_list
    
    @staticmethod
    def get_image(image_id: str) -> Optional[Dict]:
        """
        获取单个图片信息
        
        参数:
            image_id: 图片ID
            
        返回:
            Optional[Dict]: 图片信息，如果不存在则返回None
        """
        # 查找匹配的文件
        files = list_files()
        target_file = None
        
        for filename in files:
            if filename.startswith(image_id):
                target_file = filename
                break
        
        if not target_file:
            return None
            
        file_path = os.path.join(UPLOAD_DIR, target_file)
        
        # 获取文件基本信息
        file_stats = os.stat(file_path)
        file_size = file_stats.st_size
        created_at = datetime.fromtimestamp(file_stats.st_ctime).isoformat()
        
        # 从文件名推断MIME类型
        mime_type = "image/jpeg"  # 默认
        if target_file.endswith(".png"):
            mime_type = "image/png"
        elif target_file.endswith(".gif"):
            mime_type = "image/gif"
        elif target_file.endswith(".webp"):
            mime_type = "image/webp"
        
        image_info = {
            "id": target_file.split('.')[0],  # UUID作为ID
            "filename": target_file,
            "url": f"/static/images/{target_file}",
            "size": file_size,
            "mime_type": mime_type,
            "created_at": created_at
        }
        
        return image_info
    
    @staticmethod
    def delete_image(image_id: str) -> Tuple[bool, str]:
        """
        删除图片
        
        参数:
            image_id: 图片ID
            
        返回:
            Tuple[bool, str]: (是否成功, 消息)
        """
        # 查找匹配的文件
        files = list_files()
        target_file = None
        
        for filename in files:
            if filename.startswith(image_id):
                target_file = filename
                break
        
        if not target_file:
            return False, "图片不存在"
            
        return delete_file(target_file) 