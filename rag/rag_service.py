"""
rag总结服务类：
搜索提问，搜索参考资料，将提问和参考资料提交给模型，模型总结回复
"""
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from rag.vector_store import  VectorStoreService
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from utils.prompt_loader import load_rag_prompt


def print_prompt(prompt):
    print("prompt:" + "=" * 50)
    print(prompt)
    print("prompt end" + "=" * 50)
    return prompt


class RagSummarizeService(object):
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.retriever = self.vector_store.get_retriever()
        self.prompt_text = load_rag_prompt()
        self.prompt_template = PromptTemplate.from_template(self.prompt_text)
        self.model = chat_model
        self.chain = (self.__init__chian())

    def __init__chian(self):
        chain = self.prompt_template | print_prompt | self.model | StrOutputParser()
        return chain

    def retriever_docs(self, query) -> list[Document]:
        return self.retriever.invoke(query)

    def rag_summarize(self, query: str) -> str:
        """
        :param query: 提问
        :return: 总结
        """
        context_docs = self.retriever_docs(query)
        context = ""
        count = 0
        for doc in context_docs:
            count += 1
            context += f"[参考资料{count}]：参考资料：{doc.page_content}|参考元数据：{doc.metadata}\n"
        return self.chain.invoke({"input": query, "context": context})


if __name__ == '__main__':
    rag_service = RagSummarizeService()
    print(rag_service.rag_summarize("小户型适合哪些扫地机器人？"))
