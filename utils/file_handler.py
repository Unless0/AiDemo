"""
文件处理
"""
import os
from langchain_core.documents import Document
from utils.logger_handler import logger
import hashlib as hl
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def get_file_md5_hex(file_path) -> str:
    """
    获取文件的md5哈希值 十六进制字符串
    :return:
    """
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件{file_path}不存在")
        return None
    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径:{file_path}不是文件")
        return None
    # 创建MD5对象
    md5_obj = hl.md5(file_path.encode('utf-8'))

    # 4096分片大小，避免文件过大
    chunk_size = 4096
    try:
        # 计算md5必须二进制读取
        with open(file_path, "rb") as f:
            """
              := 等价于
              chunk = f.read(chunk_size)
              while chunk:
                  md5_obj.update(chunk)
                  chunk = f.read(chunk_size)
              """
            while chunk := f.read(chunk_size):
                md5_obj.update(chunk)
            # 计算MD5哈希值并以十六进制字符串形式
            md5_hex = md5_obj.hexdigest()
            return md5_hex
    except Exception as e:
        logger.error(f"计算文件{file_path}md5失败，{str(e)}")
        return None


def listdir_with_allowed_type(path: str, allowed_type: tuple[str]):
    """
    返回文件夹内的文件列表，允许的文件后缀
    :return:
    """
    files = []
    if not os.path.isdir(path):
        logger.error(f"[listdir_with_allowed_type]:{path}不是文件夹")
        return allowed_type
    for file in os.listdir(path):
        # 判断文件类型
        if file.split(".")[-1] in allowed_type:
            files.append(os.path.join(path, file))
    # tuple类型是不允许被修改的
    return tuple(files)


def pdf_loader(file_path: str, password: str = None) -> list[Document]:
    """
    pdf文件加载
    :return:
    """
    loader = PyPDFLoader(file_path=file_path, password=password)
    return loader.load()


def text_loader(file_path: str) -> list[Document]:
    """
    文本文件加载
    :return:
    """
    loader = TextLoader(file_path=file_path,encoding="utf-8")
    return loader.load()
