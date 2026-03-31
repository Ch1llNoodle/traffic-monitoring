from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
from loguru import logger
import os
import uuid
import werkzeug.utils
from typing import Tuple, Dict, Any

from config import FILE_STORE_CONFIG, PORT

app = Flask(__name__)
CORS(app)

def sanitize_path(path: str) -> str:
    """确保路径安全，避免路径遍历攻击"""
    return werkzeug.utils.safe_join(FILE_STORE_CONFIG['base_path'], path)

def ensure_directory(bucket_name: str) -> str:
    """确保存储目录存在"""
    directory = os.path.join(FILE_STORE_CONFIG['base_path'], bucket_name)
    os.makedirs(directory, exist_ok=True)
    return directory

@app.route('/api/file/upload/<bucket>', methods=['POST'])
def upload_file(bucket: str) -> Tuple[Response, int]:
    """上传文件"""
    if 'file' not in request.files:
        return jsonify({'code': 400, 'msg': '没有文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'code': 400, 'msg': '没有选择文件'}), 400
    
    logger.info(f"Uploading file: {file.filename}, type: {file.content_type}")
    
    # 验证文件类型
    if file.content_type not in FILE_STORE_CONFIG['allowed_types']:
        logger.warning(f"Unsupported file type: {file.content_type}")
        return jsonify({'code': 400, 'msg': '不支持的文件类型'}), 400
    
    # 读取并验证文件大小
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > FILE_STORE_CONFIG['max_size']:
        logger.warning(f"File too large: {file_size}")
        return jsonify({'code': 400, 'msg': '文件大小超过限制'}), 400
    
    # 确定文件名
    is_cache = request.form.get('is_cache') == 'true'
    
    if is_cache:
        filename = werkzeug.utils.secure_filename(file.filename)
    else:
        extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{extension}"
    
    directory = ensure_directory(bucket)
    file_path = os.path.join(directory, filename)
    
    file.save(file_path)
    logger.info(f"File saved to: {file_path}")
    
    # 返回文件访问URL
    url = f"{FILE_STORE_CONFIG['access_url']}/{bucket}/{filename}"
    return jsonify({
        'code': 200,
        'msg': '上传成功',
        'data': {
            'url': url,
            'bucket': bucket,
            'objectKey': filename
        }
    })

@app.route('/api/file/<bucket>/<object_key>', methods=['GET'])
def get_file(bucket: str, object_key: str) -> Response:
    """获取文件"""
    file_path = sanitize_path(os.path.join(bucket, object_key))
    if not file_path or not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}")
        return jsonify({'code': 404, 'msg': '文件不存在'}), 404
    return send_file(file_path)

@app.route('/api/file/<bucket>/<object_key>', methods=['DELETE'])
def delete_file(bucket: str, object_key: str) -> Response:
    """删除文件"""
    file_path = sanitize_path(os.path.join(bucket, object_key))
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        logger.info(f"File deleted: {file_path}")
    return jsonify({
        'code': 200,
        'msg': '删除成功'
    })

if __name__ == '__main__':
    os.makedirs(FILE_STORE_CONFIG['base_path'], exist_ok=True)
    logger.info(f"File storage service started on port {PORT}")
    app.run(host='0.0.0.0', port=PORT) 
