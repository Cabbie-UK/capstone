__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# modules/tools.py
import os
import json
from crewai_tools import tool
from serpapi.google_search import GoogleSearch
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Initialize vector store
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma(
    collection_name="rental_info",
    embedding_function=embeddings_model,
    persist_directory="./chroma_langchain_db"
)
retriever = vector_store.as_retriever(k=5)

@tool("search_rental_info")
def search_rental_info(query: str) -> str:
    """
    Search through rental information using the query provided.
    Useful for finding specific details about rentals, policies, or procedures.
    """
    docs = retriever.invoke(query)
    results = [f"Result {i+1}:\n{doc.page_content}\n" for i, doc in enumerate(docs)]
    return "\n".join(results)

@tool("serpapi_search")
def serpapi_search(query: str) -> list:
    """Search using SerpAPI and return top URLs."""
    api_key = os.environ['SERPAPI_API_KEY']
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "location": "Singapore",
        "hl": "en",
        "num": 4
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return [result['link'] for result in results.get("organic_results", [])]

@tool("read_json_file")
def read_json_file(file_path: str) -> dict:
    """Read JSON file and return its contents."""
    try:
        if isinstance(file_path, dict):
            # Handle the case where file_path is passed as a dictionary
            file_path = file_path.get('file_path', '')
        
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {str(e)}")
