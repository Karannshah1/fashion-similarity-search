import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import pinecone
import numpy as np
import requests

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)




# Connect to Pinecone
api = "aa16c305-0361-4313-98a6-1058b286fdec"

pinecone.init(api_key = api,environment='us-west4-gcp-free')
index_name = 'first'

# API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-base-uncased"
# headers = {"Authorization": f"Bearer {api}"}

# def query(payload):
# 	response = requests.post(API_URL, headers=headers, json=payload)
# 	return response.json()
	
# output = query({
# 	"inputs": "The answer to the universe is [MASK].",
# })

if index_name in pinecone.list_indexes():
  pinecone.delete_index(index_name)

dimensions = 768

pinecone.create_index(name = index_name, dimension = dimensions,metric = 'cosine')
index = pinecone.Index(index_name=index_name)


df = pd.read_csv('result.csv')

dataset = df.to_dict('records')  # Convert DataFrame to list of dictionaries

# Index the dataset
id_vector_map = {}

embedding_list=[]
temp = []

vtry = []
for data_point in dataset:
    # Tokenize and encode the input
    inputs = tokenizer.encode_plus(data_point['clean_text'], add_special_tokens=True, return_tensors='pt')

    
    # Pass the tokenized input through the BERT model
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.squeeze(0)

        pooled_embedding = torch.mean(embedding, dim=0)
        
    temp.append(str(data_point['clean_text']))
    vtry.append(pooled_embedding.numpy().astype(np.float32).tolist())
    
index.upsert(vectors = zip(temp,vtry))



