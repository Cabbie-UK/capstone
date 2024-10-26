# Import relevant packages
import os
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from openai import OpenAI
import tiktoken

# load environment variables via the .env file
load_dotenv('.env')

# Pass the API Key to the OpenAI Client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Function to generate embeddings
def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]

# Function for text generation
# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=256, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None
    
    messages = [{"role": "user", "content": prompt}]

    response = client.chat.completions.create( #originally was openai.chat.completions
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1,
        response_format=output_json_structure,
    )
    return response.choices[0].message.content

# Function for text generation from messages
# This a "modified" helper function that we will discuss in this session
# Note that this function directly take in "messages" as the parameter.

def get_completion_from_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content

# These functions are for calculating the tokens.
# ⚠️ These are simplified implementations that are good enough for a rough estimation.

def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))

def count_tokens_from_message(messages):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    value = ' '.join([x.get('content') for x in messages])
    return len(encoding.encode(value))


# Retrieve function for tax relief
def get_chatbot_response(prompt, retriever, messages):
  # Combine all previous messages into a single string
  conversation_history = "\n".join([msg["content"] for msg in messages])
  # Prepend conversation history to the prompt
  full_prompt = f"{conversation_history}\n{prompt}"
  
  retriever = retriever
  qa_chain = RetrievalQA.from_chain_type(
      llm=ChatOpenAI(model="gpt-4o-mini"),
      retriever=retriever,
      chain_type="stuff"
  )
  vector_response = qa_chain.invoke({"query": full_prompt})
  if vector_response and "result" in vector_response:
    return vector_response["result"].replace("$", "\\$")
  else:
    return "I couldn't find an exact match for your query, but feel free to ask more."


