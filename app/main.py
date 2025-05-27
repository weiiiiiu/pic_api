import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from app.routers import images

# 创建FastAPI应用
app = FastAPI(
    title="图片上传API",
    description="一个简单的图片上传、获取、删除API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板
templates = Jinja2Templates(directory="templates")

# 添加路由
app.include_router(images.router)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    首页 - 图片上传测试页面
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "ok", "message": "服务正常运行"}

if __name__ == "__main__":
    import uvicorn
    
    # 确保图片存储目录存在
    os.makedirs("static/images", exist_ok=True)
    
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 