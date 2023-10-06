# fashion-similarity-search
This is machine learning model which is taking query and in result URLs related to semantic search is displayed based on dataset.

## Installation of application

<b>Step 1:</b><br>
To install relevant libraries necessary for the given application run the following command in terminal (make sure you are in the same directory in which all the codes are stored)
```bash
pip install -r requirements.txt
```
<b>Step 2:</b><br>
Run the following program in the terminal. you only need to run this command when running the code for the first time
```bash
python web_scrapping.py
python similarity_code.py
```

<b>Step 3:</b><br>
Run the following command on Terminal to open the application
```bash
flask --app app run
```

## APIs used for application
[Pinecone](https://www.pinecone.io/): Provides an efficient way to store and retrieve the most relevant<br>
[Hugging Face](http://hf.co/settings/tokens): To retrieve Vector embeddings of given document


Requirements: 

Numpy
Hugging face (BERT)<br>
tranformers<br>
pincecone<br>
pytorch<br>
selenium <br>
pandas <br>
BeautifulSoup <br>
nltk<br>
