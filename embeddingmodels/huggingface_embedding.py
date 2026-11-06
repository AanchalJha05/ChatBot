from langchain_huggingface import HuggingFaceEmbeddings
embedding= HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)
texts = [
    "hello this is abcd",
    "hello your name is vs assistance",
    "and you all are very beautiful"

]
vector = embedding.embed_documents(texts)
print(vector)