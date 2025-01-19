import os
import openai
import requests
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import pandas as pd
from qdrant_client import models, QdrantClient
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv


load_dotenv()

df = pd.read_csv('../wine-ratings.csv')
df = df[df['variety'].notna()] # remove any NaN values as it blows up serialization
data = df.sample(700).to_dict('records') # Get only 700 records. More records will make it slower to index


app = FastAPI()

openai.api_base = os.getenv("LLAMAFILE_API_URL")  # Your Azure OpenAI resource's endpoint value.
openai.api_key = os.getenv("LLAMAFILE_API_KEY")

api_url = os.getenv("LLAMAFILE_API_URL") + "/v1/chat/completions"
api_key = os.getenv("LLAMAFILE_API_KEY")
headers = {"Authorization": f"Bearer {api_key}"}
model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant = QdrantClient(":memory:")  # In-memory instance

collection_name = "wine_ratings"
qdrant.recreate_collection(
    collection_name=collection_name,
    vectors_config=models.VectorParams(
    size=model.get_sentence_embedding_dimension(), 
    distance=models.Distance.COSINE)
)

qdrant.upload_points(
    collection_name=collection_name,
    points=[
        models.PointStruct(
            id=idx,
            vector= model.encode(doc['notes']).tolist(),
            payload=doc,
        ) for idx, doc in enumerate(data) # data is the variable holding all the wines
    ]
)

class Body(BaseModel):
    query: str


@app.get('/')
def root():
    return RedirectResponse(url='/docs', status_code=301)


@app.post('/ask')
def ask(body: Body):
    """
    Use the query parameter to interact with the Azure OpenAI Service
    using the Azure Cognitive Search API for Retrieval Augmented Generation.
    """
    search_result = search(body.query)
    chat_bot_response = assistant(body.query, search_result)
    return {'response': chat_bot_response}



def search(query):
    """
    Send the query to Azure Cognitive Search and return the top result
    """
    docs = qdrant.search(
        collection_name= collection_name,
        query_vector=model.encode(query).tolist(),
        limit=5
    )
    result = [doc.payload for doc in docs]
    print(result)
    return result
import math

def clean_floats(data):
    """
    Recursively sanitize a data structure to replace NaN, Infinity, and -Infinity with valid JSON values.
    """
    if isinstance(data, list):
        return [clean_floats(item) for item in data]
    elif isinstance(data, dict):
        return {key: clean_floats(value) for key, value in data.items()}
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return 0.0  # Replace invalid floats with 0.0
    return data


def assistant(query, context):
    sanitized_context = clean_floats(context)
    search_summary = "\n".join([
        f"Name: {item.get('name', 'Unknown')}, "
        f"Region: {item.get('region', 'Unknown')}, "
        f"Rating: {item.get('rating', 'N/A')}, "
        f"Notes: {item.get('notes', 'No notes available')}"
        for item in sanitized_context
    ])
    payload = {
        "model": "LLaMA_CPP",
        "messages": [
            {"role": "system", "content": "You are a chatbot, a wine specialist. Your top priority is to help guide users into selecting amazing wine and guide them with their requests."},
            {"role": "user", "content": query},
            {"role": "assistant", "content": search_summary}
        ]
    }

    # Make the POST request
    response = requests.post(f"{api_url}", json=payload, headers=headers)

    # Check the response
    print(response.status_code)
    if response.status_code == 200:
        completion = response.json()
        return completion['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code}, {response.text}"


