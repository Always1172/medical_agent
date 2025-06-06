import chromadb
from langchain_community.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma

# 初始化 Chroma
client = chromadb.Client()
embedding = OpenAIEmbeddings()

# 读取 Chroma 向量存储
chroma_store = Chroma(embedding_function=embedding, persist_directory= r"C:\Users\10505\Desktop\medical-agent\data\knowledge_base")
print(chroma_store._collection.count())
llm = ChatOpenAI(model='gpt-4o', temperature=0)

# 使用 Chroma
rag_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=chroma_store.as_retriever())

def rag_qa(query):
    return rag_chain.invoke({"query": query})

# 使用示例
if __name__ == "__main__":
    query = "Always1172的住址是哪里"
    result = rag_qa(query)
    print(result)