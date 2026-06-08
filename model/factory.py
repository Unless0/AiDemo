"""
工厂：抽象 ，模型
"""
from abc import ABC, abstractmethod
from typing import Optional
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel, ChatTongyi
from utils.config_handler import rag_conf
from langchain_community.embeddings import DashScopeEmbeddings


class BaseMModelFactory(ABC):
    @abstractmethod
    def gennerator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatmodelFactory(BaseMModelFactory):
    def gennerator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(model=rag_conf["chat_model_name"])


class EmbeddingFactory(BaseMModelFactory):
    def gennerator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(model=rag_conf["embedding_model_name"])

chat_model=ChatmodelFactory().gennerator()
embedding_model=EmbeddingFactory().gennerator()
