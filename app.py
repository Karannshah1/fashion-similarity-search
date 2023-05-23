from flask import Flask, jsonify, request

app = Flask(__name__)

model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

api = "aa16c305-0361-4313-98a6-1058b286fdec"

pinecone.init(api_key = api,environment='us-west4-gcp-free')
index_name = 'first'

@app.route('/', methods=['GET','POST'])
def process_request():
    # Get the input text from the JSON payload
    input_text = request.json['input_text']

    # Perform similarity search and retrieve the ranked list of similar item URLs
    # Replace this with your actual code for similarity search


    query = input_text
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
    similar_items = []
    for i in response.results[0].matches:
      similar_results.append(i.id)
      indices.append(i.score)

    #extracting results
    results = [data_point for data_point in dataset if str(data_point['id']) in similar_results]

   
    # Return the ranked list of similar item URLs as a JSON response
    return jsonify({'similar_items': results})

if __name__ == '__main__':
    app.run()
