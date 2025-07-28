from . import httpclient
from .const import base_url,files_url

__all__ = ['http_get', 'http_post', 'http_upload', 'download_file','base_url','file_url'],

# 将httpclient中的函数导入到当前包的命名空间
from .httpclient import (
    http_get,
    http_post,
    http_upload,
    download_file,
)

from .const import (
    base_url,
    files_url,
)