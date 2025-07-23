import chromadb
# 替换原有的from dracary.config.load import load_config
from dracary.config.load import ConfigLoader
from dracary.retrieval.chroma import EmbeddingClient, ChromaVectorStore
# 1. 加载配置
config_loader = ConfigLoader()
config = config_loader.config
embedding_config = config["embedding_api"]

# 2. 初始化工具客户端
embedding_client = EmbeddingClient(
    api_url=embedding_config["url"],
    api_key=embedding_config["api_key"],
    model=embedding_config["model"]
)
vector_store = ChromaVectorStore()

# 3. 文档处理示例
if __name__ == "__main__":
    documents = [
        "This is a document about pineapple",
        "This is a document about oranges"
    ]

    # 获取嵌入向量
    embeddings = embedding_client.batch_get_embeddings(documents)
    print("已完成向量化。")

    # 存入向量数据库
    collection = vector_store.create_collection("my_collection")
    vector_store.add_documents(
        collection_name="my_collection",
        documents=documents,
        embeddings=embeddings,
        ids=[f"id{i}" for i in range(len(documents))]
    )
    print("已完成向量化并存入 chromadb。")
