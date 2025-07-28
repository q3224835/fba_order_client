import requests
import os
from typing import Optional, Dict, Any, BinaryIO

def http_get(url: str, params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str,str]] = None,
             timeout: int = 30) -> Dict[str, Any]:
    """
    发送application/json格式的GET请求
    
    :param url: 请求URL
    :param params: 查询参数
    :param headers: 请求头
    :param timeout: 超时时间(秒)
    :return: 响应的JSON数据
    :raises: requests.exceptions.RequestException 请求异常
    """
    default_headers = { "Content-Type": "application/json" }
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(url, 
                                params=params, 
                                headers=default_headers, 
                                timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP GET request failed: {e}")
    
def http_post(url:str,data:Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str,str]] = None,
              timeout: int = 30) -> Dict[str, Any]:
    """
    发送application/json格式的POST请求
    
    :param url: 请求URL
    :param data: 发送的JSON数据
    :param headers: 请求头
    :param timeout: 超时时间(秒)
    :return: 响应的JSON数据
    :raises: requests.exceptions.RequestException 请求异常
    """
    default_headers = [{ "Content-Type": "application/json" }]
    if headers:
        default_headers.append(headers)
    
    try:
        response = requests.post(url, 
                                data=data, 
                                headers=default_headers, 
                                timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP POST request failed: {e}")
    
def http_upload(url: str, file_stream: BinaryIO,
                file_name: str, params:Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str,str]] = None,
                timeout: int = 60) -> Dict[str, Any]:
    """
    上传文件(文件流形式)
    
    :param url: 上传URL
    :param file_stream: 文件流对象
    :param file_name: 文件名
    :param params: 额外的表单参数
    :param headers: 请求头
    :param timeout: 超时时间(秒)
    :return: 响应的JSON数据
    :raises: requests.exceptions.RequestException 请求异常
    """
    files = { "file": (file_name, file_stream) }
    try:
        response = requests.post(
            url,
            files=files,
            params=params,
            headers=headers,
            timeout=timeout
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP POST request failed: {e}")
    finally:
        file_stream.close()

def download_file(url: str, file_path: str,
                 params: Optional[Dict[str, Any]] = None,
                 headers: Optional[Dict[str,str]] = None,
                 timeout: int = 60) -> None:
    """
    下载文件(文件流形式)
    
    :param url: 下载URL
    :param save_path: 保存文件路径
    :param params: 请求参数
    :param headers: 请求头
    :param timeout: 超时时间(秒)
    :return: 保存的文件路径
    :raises: requests.exceptions.RequestException 请求异常
             IOError  文件操作异常
    """
    try:
        with requests.get(url, stream=True, params=params, headers=headers, timeout=timeout) as response:
            response.raise_for_status()
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        return file_path
    except requests.RequestException as e:
        raise RuntimeError(f"HTTP GET request failed: {e}")
    except IOError as e:
        raise RuntimeError(f"File operation failed: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
