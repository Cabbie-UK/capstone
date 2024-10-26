import streamlit as st
from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
# ================== Note =================
# This script Is meant to set up the vector store for info retrieval
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


# ================== Setup Vector Store with info on Rental info =================
# - More supporting documents can be loaded
# - Loading, Splitting approach can changed 

# # 1. Document loading
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import PyPDFLoader

# Usage:

# A. Load the word document on Income_from_property_rented_out.docx
loader = Docx2txtLoader("./data/Income_from_property_rented_out.docx")
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
    collection_name="rental_info",
    documents=splitted_document_objs,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",
)

# B Load the pdf document e_tax_guide_simplified_rental_expense_claim.pdf
loader = PyPDFLoader("./data/e_tax_guide_simplifed_rental_expense_cLaim.pdf")
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
    collection_name="rental_info",
    documents=splitted_document_objs,
    embedding=embeddings_model,
    persist_directory="./chroma_langchain_db",
)



# Verify the vector store is populated by performing a search
query = "What are the non-allowable expenses against property income?"
results = vector_store.similarity_search(query, k=5)

# Display the results in Streamlit
st.write("Retrieved Documents:")
# Display the content of the retrieved documents
for i, result in enumerate(results):
    st.write(f"Document {i+1}:")
    st.write(result.page_content)  
