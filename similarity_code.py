import pandas as pd
from transformers import BertTokenizer, BertModel
import torch
import pinecone
import numpy as np

# Load pre-trained BERT model and tokenizer
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Connect to Pinecone
api = "aa16c305-0361-4313-98a6-1058b286fdec"

pinecone.init(api_key = api,environment='us-west4-gcp-free')
index_name = 'first'

if index_name in pinecone.list_indexes():
  pinecone.delete_index(index_name)

dimensions = 768

pinecone.create_index(name = index_name, dimension = dimensions,metric = 'cosine')
index = pinecone.Index(index_name=index_name)
# index_name = "your_index_name"
# index = pinecone.Index(index_name=index_name)

# Load dataset from CSV file
# dataset_path = "path/to/your/dataset.csv"
# df = pd.read_csv(dataset_path)

# df = pd.DataFrame(dataset)

# # Example dataset

df = pd.read_csv('result.csv')

dataset = df.to_dict('records')  # Convert DataFrame to list of dictionaries

# Index the dataset
id_vector_map = {}

embedding_list=[]
temp = []

vtry = []
for data_point in dataset:
    # Tokenize and encode the input
    inputs = tokenizer.encode_plus(data_point['id'], add_special_tokens=True, return_tensors='pt')

    
    # Pass the tokenized input through the BERT model
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state.squeeze(0)

        pooled_embedding = torch.mean(embedding, dim=0)
        
    temp.append(str(data_point['id']))
    vtry.append(pooled_embedding.numpy().astype(np.float32).tolist())
    
index.upsert(vectors = zip(temp,vtry))


# Perform similarity search
query = "Men formal shoes"
query_inputs = tokenizer.encode_plus(query, add_special_tokens=True, return_tensors='pt')
with torch.no_grad():
    query_outputs = model(**query_inputs)
    query_embedding = query_outputs.last_hidden_state.squeeze(0)

    query_pooled_list = torch.mean(query_embedding, dim=0).numpy()

    

# Retrieve similar results from Pinecone
query_embedding_list = query_pooled_list.tolist()

# Retrieve similar results from Pinecone

response = index.query(queries=[query_embedding_list], top_k=5)
print(response)
similar_results = []
indices = []
for i in response.results[0].matches:
  similar_results.append(i.id)
  indices.append(i.score)



# Retrieve the corresponding data points from the database using the identifiers
results = [data_point for data_point in dataset if str(data_point['id']) in similar_results]

print(results,indices)
