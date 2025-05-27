# 图片上传服务 (PicApi)

一个简单的图片上传、获取、删除 API 服务，可用于小程序的图床服务。

## 功能特点

- 图片上传：支持常见图片格式（JPG、PNG、GIF、WebP）
- 图片获取：提供图片信息和下载链接
- 图片删除：支持删除已上传的图片
- 图片管理：提供图片管理界面
- RESTful API：标准化的 API 接口
- 响应式设计：适配不同设备屏幕

## 技术栈

- 后端：Python + FastAPI
- 前端：HTML + CSS + JavaScript
- 存储：本地文件系统

## 安装与运行

### 系统要求

- Python 3.6+
- pip（Python 包管理器）

### 安装步骤

1. 克隆代码库

   ```bash
   git clone https://github.com/yourusername/pic_api.git
   cd pic_api
   ```

2. 安装依赖

   ```bash
   pip install -r requirements.txt
   ```

3. 运行服务

   ```bash
   python -m app.main
   ```

4. 访问服务
   - 在浏览器中打开 `http://localhost:8000` 查看管理界面
   - API 文档：`http://localhost:8000/docs`

## API 文档

### 上传图片

```
POST /api/images
```

请求参数：

- `file`: 要上传的图片文件（multipart/form-data）

响应示例：

```json
{
  "success": true,
  "message": "图片上传成功",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "example.jpg",
    "url": "/static/images/550e8400-e29b-41d4-a716-446655440000.jpg",
    "size": 123456,
    "mime_type": "image/jpeg",
    "created_at": "2023-09-01T12:00:00"
  }
}
```

### 获取图片列表

```
GET /api/images
```

响应示例：

```json
{
  "success": true,
  "message": "获取图片列表成功",
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "filename": "550e8400-e29b-41d4-a716-446655440000.jpg",
      "url": "/static/images/550e8400-e29b-41d4-a716-446655440000.jpg",
      "size": 123456,
      "mime_type": "image/jpeg",
      "created_at": "2023-09-01T12:00:00"
    }
  ]
}
```

### 获取单个图片信息

```
GET /api/images/{image_id}
```

路径参数：

- `image_id`: 图片 ID

响应示例：

```json
{
  "success": true,
  "message": "获取图片成功",
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "filename": "550e8400-e29b-41d4-a716-446655440000.jpg",
    "url": "/static/images/550e8400-e29b-41d4-a716-446655440000.jpg",
    "size": 123456,
    "mime_type": "image/jpeg",
    "created_at": "2023-09-01T12:00:00"
  }
}
```

### 下载图片

```
GET /api/images/{image_id}/download
```

路径参数：

- `image_id`: 图片 ID

响应：

- 文件内容（图片文件）

### 删除图片

```
DELETE /api/images/{image_id}
```

路径参数：

- `image_id`: 图片 ID

响应示例：

```json
{
  "success": true,
  "message": "文件删除成功",
  "data": null
}
```

## 在小程序中使用

在微信小程序中，可以使用 `wx.uploadFile` 和 `wx.request` 方法来调用这些 API：

```javascript
// 上传图片
wx.chooseImage({
  success(res) {
    const tempFilePaths = res.tempFilePaths;

    wx.uploadFile({
      url: "http://your-server-url/api/images",
      filePath: tempFilePaths[0],
      name: "file",
      success(res) {
        const data = JSON.parse(res.data);
        console.log(data);
      },
    });
  },
});

// 获取图片列表
wx.request({
  url: "http://your-server-url/api/images",
  method: "GET",
  success(res) {
    console.log(res.data);
  },
});
```

## 注意事项

- 本服务默认使用本地文件系统存储图片，生产环境建议使用对象存储服务
- 默认最大文件大小限制为 10MB
- 支持的图片格式：JPG、JPEG、PNG、GIF、WebP

## 许可证

MIT
