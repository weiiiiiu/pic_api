// 当DOM加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    const fileInput = document.getElementById('file-input');
    const uploadForm = document.getElementById('upload-form');
    const uploadBtn = document.getElementById('upload-btn');
    const imageGrid = document.getElementById('image-grid');
    const messageContainer = document.getElementById('message-container');
    
    // 初始化 - 加载图片列表
    loadImages();
    
    // 文件选择事件
    fileInput.addEventListener('change', function() {
        uploadBtn.disabled = !fileInput.files.length;
    });
    
    // 表单提交事件
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // 检查是否选择了文件
        if (!fileInput.files.length) {
            showMessage('请选择要上传的图片', 'error');
            return;
        }
        
        const file = fileInput.files[0];
        
        // 检查文件类型
        if (!file.type.startsWith('image/')) {
            showMessage('请选择图片文件', 'error');
            return;
        }
        
        // 上传文件
        uploadImage(file);
    });
});

/**
 * 上传图片
 * @param {File} file 要上传的文件
 */
function uploadImage(file) {
    // 显示加载状态
    showLoader();
    
    // 创建FormData对象
    const formData = new FormData();
    formData.append('file', file);
    
    // 发送请求
    fetch('/api/images', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        // 隐藏加载状态
        hideLoader();
        
        if (data.success) {
            // 显示成功消息
            showMessage(data.message, 'success');
            
            // 重置表单
            document.getElementById('upload-form').reset();
            document.getElementById('upload-btn').disabled = true;
            
            // 重新加载图片列表
            loadImages();
        } else {
            // 显示错误消息
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        // 隐藏加载状态
        hideLoader();
        
        // 显示错误消息
        showMessage('上传失败: ' + error.message, 'error');
    });
}

/**
 * 加载图片列表
 */
function loadImages() {
    // 显示加载状态
    showLoader();
    
    // 获取图片列表容器
    const imageGrid = document.getElementById('image-grid');
    
    // 发送请求
    fetch('/api/images')
    .then(response => response.json())
    .then(data => {
        // 隐藏加载状态
        hideLoader();
        
        if (data.success) {
            // 清空列表
            imageGrid.innerHTML = '';
            
            if (data.data.length === 0) {
                // 没有图片
                imageGrid.innerHTML = '<p>暂无图片</p>';
                return;
            }
            
            // 遍历图片列表
            data.data.forEach(image => {
                // 创建图片卡片
                const card = createImageCard(image);
                
                // 添加到列表
                imageGrid.appendChild(card);
            });
        } else {
            // 显示错误消息
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        // 隐藏加载状态
        hideLoader();
        
        // 显示错误消息
        showMessage('加载图片列表失败: ' + error.message, 'error');
    });
}

/**
 * 创建图片卡片
 * @param {Object} image 图片信息
 * @returns {HTMLElement} 图片卡片元素
 */
function createImageCard(image) {
    // 创建卡片容器
    const card = document.createElement('div');
    card.className = 'image-card';
    card.dataset.id = image.id;
    
    // 图片预览
    const preview = document.createElement('img');
    preview.className = 'image-preview';
    preview.src = image.url;
    preview.alt = image.filename;
    card.appendChild(preview);
    
    // 图片信息
    const info = document.createElement('div');
    info.className = 'image-info';
    
    // 文件名
    const name = document.createElement('h3');
    name.textContent = image.filename;
    name.title = image.filename;
    info.appendChild(name);
    
    // 文件大小
    const size = document.createElement('p');
    size.textContent = '大小: ' + formatFileSize(image.size);
    info.appendChild(size);
    
    // 上传时间
    const time = document.createElement('p');
    time.textContent = '上传时间: ' + formatDate(image.created_at);
    info.appendChild(time);
    
    // 操作按钮
    const actions = document.createElement('div');
    actions.className = 'image-actions';
    
    // 下载按钮
    const downloadBtn = document.createElement('a');
    downloadBtn.className = 'btn btn-download';
    downloadBtn.href = `/api/images/${image.id}/download`;
    downloadBtn.textContent = '下载';
    actions.appendChild(downloadBtn);
    
    // 删除按钮
    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'btn btn-delete';
    deleteBtn.textContent = '删除';
    deleteBtn.addEventListener('click', function() {
        deleteImage(image.id);
    });
    actions.appendChild(deleteBtn);
    
    info.appendChild(actions);
    card.appendChild(info);
    
    return card;
}

/**
 * 删除图片
 * @param {string} id 图片ID
 */
function deleteImage(id) {
    // 确认删除
    if (!confirm('确定要删除这张图片吗？')) {
        return;
    }
    
    // 显示加载状态
    showLoader();
    
    // 发送请求
    fetch(`/api/images/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        // 隐藏加载状态
        hideLoader();
        
        if (data.success) {
            // 显示成功消息
            showMessage(data.message, 'success');
            
            // 移除图片卡片
            const card = document.querySelector(`.image-card[data-id="${id}"]`);
            if (card) {
                card.remove();
            }
            
            // 检查是否还有图片
            const imageGrid = document.getElementById('image-grid');
            if (imageGrid.children.length === 0) {
                imageGrid.innerHTML = '<p>暂无图片</p>';
            }
        } else {
            // 显示错误消息
            showMessage(data.message, 'error');
        }
    })
    .catch(error => {
        // 隐藏加载状态
        hideLoader();
        
        // 显示错误消息
        showMessage('删除失败: ' + error.message, 'error');
    });
}

/**
 * 显示消息
 * @param {string} text 消息文本
 * @param {string} type 消息类型 (success 或 error)
 */
function showMessage(text, type) {
    const messageContainer = document.getElementById('message-container');
    messageContainer.innerHTML = '';
    
    const message = document.createElement('div');
    message.className = `message message-${type}`;
    message.textContent = text;
    
    messageContainer.appendChild(message);
    
    // 5秒后自动隐藏
    setTimeout(() => {
        message.remove();
    }, 5000);
}

/**
 * 显示加载状态
 */
function showLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'block';
    }
}

/**
 * 隐藏加载状态
 */
function hideLoader() {
    const loader = document.getElementById('loader');
    if (loader) {
        loader.style.display = 'none';
    }
}

/**
 * 格式化文件大小
 * @param {number} bytes 字节数
 * @returns {string} 格式化后的文件大小
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * 格式化日期
 * @param {string} dateString ISO格式的日期字符串
 * @returns {string} 格式化后的日期
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    
    return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
} 