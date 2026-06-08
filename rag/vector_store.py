"""
向量存储服务
"""
import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from model.factory import embedding_model
from utils.file_handler import pdf_loader, text_loader, listdir_with_allowed_type, get_file_md5_hex
from utils.logger_handler import logger
from utils.config_handler import chroma_conf
from utils.path_tool import get_abs_path
class VectorStoreService:
    def __init__(self):
        self.vector_store = Chroma(
            collection_name=chroma_conf['cellection_name'],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_conf['persist_directory']),
        )
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=chroma_conf['chunk_size'],
            chunk_overlap=chroma_conf['chunk_overlap'],
            separators=chroma_conf["separators"],
            length_function=len
        )

    #  检索器
    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_conf["k"]})

    def load_document(self):
        """
        从数据文件夹类读取文件，转为向量存入向量数据
        1.计算文件的md5值进行去重
        2.将文件内容切分为多个小片段，每个片段计算向量存入向量数据库

        :return:
        """

        def chunk_md5_hex(md5_str: str) -> bool:
            if not os.path.exists(get_abs_path(chroma_conf["md5_hex_store"])):
                # 如果文件不存在，则创建
                open(get_abs_path(chroma_conf["md5_hex_store"]), 'w', encoding="utf-8").close()
                return False
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'r', encoding="utf-8") as f:
                for line in f.readlines():
                    line = line.strip()
                    # 如果文件已经存在，则返回True
                    if line == md5_str:
                        return True
                return False

        def save_md5(md5_str: str):
            with open(get_abs_path(chroma_conf["md5_hex_store"]), 'a', encoding="utf-8") as f:
                f.write(md5_str + "\n")

        def get_file_documents(read_path: str) -> list[Document]:
            documents = []
            if read_path.endswith(".pdf"):
                documents = pdf_loader(read_path)
            if read_path.endswith(".txt"):
                documents = text_loader(read_path)
            return documents

        allowed_file_path: list[str] = listdir_with_allowed_type(get_abs_path(chroma_conf["data_path"]),
                                                                 tuple(chroma_conf["allow_knowledge_type"]))

        for file_path in allowed_file_path:
            md5_shex = get_file_md5_hex(file_path)
            if chunk_md5_hex(md5_shex):
                logger.info(f"[加载知识库]{file_path}内容已经存在，跳过")
                continue
            try:
                documents = get_file_documents(file_path)
                if not documents:
                    logger.info(f"[加载知识库]{file_path}内容为空，跳过")
                    continue
                spliter_document: list[Document] = self.spliter.split_documents(documents)

                if not spliter_document:
                    logger.info(f"[加载知识库]{file_path}内容切分后为空，跳过")
                    continue
                # 存入向量数据库
                self.vector_store.add_documents(spliter_document)
                # 保存md5值,防止重复加载
                save_md5(md5_shex)
                logger.info(f"[加载知识库]{file_path}内容加载成功")
            except Exception as e:
                # exc_info为True 会详细记录堆栈报错信息，为False仅记录报错本身
                logger.error(f"[加载知识库]{file_path}内容加载失败，错误信息：{str(e)}", exc_info=True)


if __name__ == '__main__':
    vector_store = VectorStoreService()
    vector_store.load_document()
    retriever = vector_store.get_retriever()
    for chunk in retriever.invoke("迷路"):
        print(chunk.page_content)
        print("=" * 50)
