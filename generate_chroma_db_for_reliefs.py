import streamlit as st
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
# ================== Note =================
# This script is meant to set up the vector store for info retrieval
# This script need not be re-run everytime the app starts
# ================== ==== =================


# ================== Setup OpenAI Client =================

# Import relevant packages
import os
from dotenv import load_dotenv
from openai import OpenAI

# load environment variables via the .env file
load_dotenv('.env')

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# ================== Setup OpenAI Client =================


# ================== Setup Vector Store with info on Tax Relief =================
# - More supporting documents can be loaded
# - Loading, Splitting approach can changed 

# # 1. Document loading
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

class CustomTextLoader(BaseLoader):
    def __init__(self, file_path: str, encoding: str = 'utf-8'):
        self.file_path = file_path
        self.encoding = encoding

    def load(self):
        with open(self.file_path, 'r', encoding=self.encoding) as f:
            text = f.read()
        return [Document(page_content=text)]

# Usage
loader = CustomTextLoader("./data/type_of_reliefs.txt")
documents = loader.load()


# Splitting & chunking
text_splitter_ = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=1000,
    chunk_overlap=100,
)

splitted_documents = text_splitter_.split_text(documents[0].page_content)
splitted_document_objs = [Document(page_content=text) for text in splitted_documents]

# Embedding & vector stores
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma.from_documents(
    collection_name="various_tax_relief",
    documents=splitted_document_objs,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",
)

# Verify the vector store is populated by performing a search
query = "What are the eligible tax reliefs for NSman?"
results = vector_store.similarity_search(query, k=5)

# Display the results in Streamlit
st.write("Retrieved Documents:")
for i, result in enumerate(results):
    st.write(f"Document {i+1}:")
    st.write(result.page_content)  # Display the content of the retrieved documents
