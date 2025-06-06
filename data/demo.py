from langchain.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader, JSONLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import os

def load_documents(directory):
    documents = []
    
    # 加载TXT文件（指定UTF-8编码）
    txt_loader = DirectoryLoader(
        directory,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={'encoding': 'utf-8'}
    )
    documents.extend(txt_loader.load())
    
    # 加载PDF文件
    pdf_loader = DirectoryLoader(
        directory,
        glob="**/*.pdf",
        loader_cls=PyPDFLoader
    )
    documents.extend(pdf_loader.load())
    
    # 加载JSON文件
    json_loader = DirectoryLoader(
        directory,
        glob="**/*.json",
        loader_cls=JSONLoader,
        loader_kwargs={
            'jq_schema': '.[]',  # 根据你的JSON结构调整
            'text_content': False
        }
    )
    documents.extend(json_loader.load())
    
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """将文档分割成较小的块"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    splits = text_splitter.split_documents(documents)
    return splits

def create_vector_db(documents, persist_directory):
    """创建向量数据库并存储文档"""
    # 初始化OpenAI嵌入模型
    embeddings = OpenAIEmbeddings()
    
    # 创建并持久化Chroma向量数据库
    vectordb = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    vectordb.persist()  # 确保数据持久化到磁盘
    return vectordb

def main():
    # 配置参数
    documents_directory = r"C:\Users\10505\Desktop\medical-agent\data\documents"  # 源文档目录
    persist_directory = r"C:\Users\10505\Desktop\medical-agent\data\knowledge_base"  # 向量存储目录
    
    # 加载文档
    print("正在加载文档...")
    documents = load_documents(documents_directory)
    print(f"已加载 {len(documents)} 个文档")
    
    # 分割文档
    print("正在分割文档...")
    splits = split_documents(documents)
    print(f"分割成 {len(splits)} 个文本块")
    
    # 创建并填充向量数据库
    print("正在创建向量数据库...")
    create_vector_db(splits, persist_directory)
    print("向量数据库创建完成并已持久化")

if __name__ == "__main__":
    main()
