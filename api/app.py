from flask import Flask, render_template, request
import pinecone
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
import pandas as pd


app = Flask(__name__)

model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

api = "aa16c305-0361-4313-98a6-1058b286fdec"

pinecone.init(api_key = api,environment='us-west4-gcp-free')
index_name = 'first'

# if index_name in pinecone.list_indexes():
#   pinecone.delete_index(index_name)

# dimensions = 768

# pinecone.create_index(name = index_name, dimension = dimensions,metric = 'cosine')
index = pinecone.Index(index_name=index_name)

df = pd.read_csv('result.csv')

dataset = df.to_dict('records')

# Create Flask app
app = Flask(__name__)

def similarity_search(search_query,cnt):
    query = search_query
    
    query_inputs = tokenizer.encode_plus(query, add_special_tokens=True, return_tensors='pt')
    with torch.no_grad():
        query_outputs = model(**query_inputs)
        query_embedding = query_outputs.last_hidden_state.squeeze(0)

        query_pooled_list = torch.mean(query_embedding, dim=0).numpy()

    

    # Retrieve similar results from Pinecone
    query_embedding_list = query_pooled_list.tolist()

    # Retrieve similar results from Pinecone

    response = index.query(queries=[query_embedding_list], top_k=cnt,include_metadata = True,include_values = False)
    
    print(response)

    # return response.result[0].matches

    
        
    similar_results = []
    indices = []
    for i in response.results[0].matches:
        similar_results.append(i.id)
        indices.append(i.score)


    print(similar_results)
    # Retrieve the corresponding data points from the database using the identifiers
    # print(dataset)
    results = [data_point for data_point in dataset if data_point['clean_text'] in similar_results]
    
    print(results)
    return results



# Define a route for the home page
@app.route('/', methods=['GET', 'POST'])

def serve_page(name = None):
    if request.method == 'POST':
        prompt = request.form.get("prompt")
        result_count = request.form.get("count")
        if(prompt == "" or type(prompt) != type("str")):
            return render_template('index.html', variable = [])
        result_count = int(result_count)
        print(prompt, result_count)
        # vec = query(prompt)
        ret = similarity_search(prompt, result_count)
        # print(ret["matches"])
        print(ret)
        return render_template('index.html', variable = ret)
    return render_template('index.html', variable = [])



# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
