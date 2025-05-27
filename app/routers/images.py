from typing import Dict, List, Optional
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Path
from fastapi.responses import FileResponse
import os

from app.services.image_service import ImageService
from app.utils.file_utils import UPLOAD_DIR

router = APIRouter(prefix="/api/images", tags=["images"])

@router.post("")
async def upload_image(file: UploadFile = File(...)):
    """
    上传图片
    """
    if not file.content_type or not file.content_type.startswith('image/'):
        return {
            "success": False,
            "message": "只允许上传图片文件",
            "data": None
        }
    
    success, message, image_info = await ImageService.upload_image(file)
    
    return {
        "success": success,
        "message": message,
        "data": image_info
    }

@router.get("")
async def get_image_list():
    """
    获取图片列表
    """
    image_list = ImageService.get_image_list()
    
    return {
        "success": True,
        "message": "获取图片列表成功",
        "data": image_list
    }

@router.get("/{image_id}")
async def get_image(image_id: str = Path(...)):
    """
    获取单个图片
    """
    image_info = ImageService.get_image(image_id)
    
    if not image_info:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    return {
        "success": True,
        "message": "获取图片成功",
        "data": image_info
    }

@router.get("/{image_id}/download")
async def download_image(image_id: str = Path(...)):
    """
    下载图片
    """
    image_info = ImageService.get_image(image_id)
    
    if not image_info:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    file_path = os.path.join(UPLOAD_DIR, image_info["filename"])
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="图片文件不存在")
    
    return FileResponse(
        path=file_path,
        filename=image_info["filename"],
        media_type=image_info["mime_type"]
    )

@router.delete("/{image_id}")
async def delete_image(image_id: str = Path(...)):
    """
    删除图片
    """
    success, message = ImageService.delete_image(image_id)
    
    return {
        "success": success,
        "message": message,
        "data": None
    } 