import os
import sys

# 获取应用程序的根目录
def get_application_root():
    """获取应用程序根目录"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        return os.path.dirname(sys.executable)
    else:
        # 如果是开发环境
        return os.path.dirname(__file__)

# 从环境变量获取主机地址，如果没有设置则默认使用localhost
HOST = os.environ.get('FILE_SERVICE_HOST', 'localhost')
PORT = int(os.environ.get('FILE_SERVICE_PORT', 5001))

# 获取文件存储路径
# 1. 首先尝试从环境变量获取
# 2. 如果环境变量未设置，则使用应用程序目录下的file_store目录
BASE_PATH = os.environ.get('FILE_STORE_PATH', os.path.join(get_application_root(), 'file_store'))

# 文件存储配置
FILE_STORE_CONFIG = {
    'base_path': BASE_PATH,
    'access_url': f'http://{HOST}:{PORT}/api/file',  # 文件访问URL前缀
    'allowed_types': [  # 支持的文件类型
        # 图片类型
        'image/jpeg',            # JPG/JPEG图片 (.jpg, .jpeg)
        'image/png',             # PNG图片 (.png)
        'image/gif',             # GIF图片 (.gif)
        'image/tiff',            # TIFF图片 (.tif, .tiff)
        'image/bmp',             # BMP图片 (.bmp)
        'image/x-ms-bmp',        # BMP图片的另一种MIME类型 (.bmp)
        'image/webp',            # WebP图片 (.webp)
        'image/x-icon',          # ICO图片 (.ico)
        'image/vnd.microsoft.icon', # ICO图片的另一种MIME类型 (.ico)
        'image/svg+xml',         # SVG图片 (.svg)
        'image/x-portable-pixmap', # PPM图片 (.ppm)
        'image/x-portable-graymap', # PGM图片 (.pgm)
        'image/x-portable-bitmap',  # PBM图片 (.pbm)
        'image/x-portable-anymap',  # PNM图片 (.pnm)
        'image/x-rgb',           # RGB图片 (.rgb)

        # 文档类型
        'application/pdf',       # PDF文档 (.pdf)
        'application/msword',    # Word文档 (.doc)
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # Word文档 (.docx)
        'text/plain',           # 纯文本文件 (.txt)
        'text/markdown',        # Markdown文档 (.md)
        'text/x-markdown',      # Markdown文档的另一种MIME类型 (.md)
        'application/json',     # JSON文件 (.json)
        'text/csv',             # CSV文件 (.csv)
        
        # 压缩包类型
        'application/zip',              # ZIP压缩包 (.zip)
        'application/x-zip-compressed', # ZIP压缩包的另一种MIME类型 (.zip)
        'application/x-gzip',    # GZIP文件 (.gz)
        'application/x-tar',     # TAR文件 (.tar)
        'application/x-bzip2',   # BZIP2文件 (.bz2)
        'application/x-rar-compressed', # RAR压缩包 (.rar)
        'application/x-7z-compressed', # 7Z压缩包 (.7z)
        
        # 深度学习模型权重文件类型
        'application/x-hdf5',           # HDF5文件 (.h5, .hdf5) - TensorFlow/Keras权重文件
        'application/octet-stream',     # 二进制文件 - 通用类型，支持.weights.h5, .pt, .pth, .ckpt等
        'application/x-tensorflow',      # TensorFlow模型文件 (.pb, .ckpt)
        'application/x-pytorch',         # PyTorch模型文件 (.pt, .pth)
        'application/x-onnx',           # ONNX模型文件 (.onnx)
        'application/x-keras',          # Keras模型文件 (.keras)
        'application/x-savedmodel'      # TensorFlow SavedModel格式
    ],
    'max_size': 1000 * 1024 * 1024  # 最大文件大小：1000MB
} 