import os
import uuid
from typing import List, Optional, Tuple
from fastapi import UploadFile

# 允许的文件类型
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
# 最大文件大小（10MB）
MAX_FILE_SIZE = 10 * 1024 * 1024
# 图片存储目录
UPLOAD_DIR = os.path.join('static', 'images')

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_allowed_file(filename: str) -> bool:
    """检查文件类型是否允许"""
    extension = get_file_extension(filename)
    return extension in ALLOWED_EXTENSIONS

def is_within_size_limit(file_size: int) -> bool:
    """检查文件大小是否在限制范围内"""
    return file_size <= MAX_FILE_SIZE

async def save_upload_file(upload_file: UploadFile) -> Tuple[bool, str, Optional[str]]:
    """
    保存上传的文件
    
    返回:
        Tuple[bool, str, Optional[str]]: (是否成功, 消息, 文件路径)
    """
    # 检查文件类型
    if not is_allowed_file(upload_file.filename):
        return False, f"不支持的文件类型，仅支持: {', '.join(ALLOWED_EXTENSIONS)}", None
    
    # 确保上传目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 生成唯一的文件名
    extension = get_file_extension(upload_file.filename)
    new_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, new_filename)
    
    # 检查文件内容
    content = await upload_file.read()
    
    # 检查文件大小
    if not is_within_size_limit(len(content)):
        return False, f"文件大小超过限制，最大允许: {MAX_FILE_SIZE / 1024 / 1024}MB", None
    
    # 保存文件
    try:
        with open(file_path, "wb") as f:
            f.write(content)
        return True, "文件上传成功", new_filename
    except Exception as e:
        return False, f"文件保存失败: {str(e)}", None

def delete_file(filename: str) -> Tuple[bool, str]:
    """
    删除文件
    
    参数:
        filename: 文件名（不包含路径）
    
    返回:
        Tuple[bool, str]: (是否成功, 消息)
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        return False, "文件不存在"
    
    # 删除文件
    try:
        os.remove(file_path)
        return True, "文件删除成功"
    except Exception as e:
        return False, f"文件删除失败: {str(e)}"

def list_files() -> List[str]:
    """
    列出所有上传的文件
    
    返回:
        List[str]: 文件名列表
    """
    # 确保上传目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    # 列出目录中的所有文件
    files = [f for f in os.listdir(UPLOAD_DIR) 
             if os.path.isfile(os.path.join(UPLOAD_DIR, f)) and 
             get_file_extension(f) in ALLOWED_EXTENSIONS]
    
    return files 