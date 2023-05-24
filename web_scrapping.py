from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer

# Set the path to the downloaded ChromeDriver executable
driver_path = 'C:/Users/91910/Downloads/chromedriver_win32/chromedriver'

chrome_options = Options()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')

# Create a new instance of the Chrome driver with the options
driver = webdriver.Chrome(options=chrome_options, executable_path=driver_path)

# Load the Meesho website
page_number = 1
url_list = ['https://www.meesho.com/tops-ladies/pl/3ja?page=','https://www.meesho.com/women-clothing/pl/9om?page=','https://www.meesho.com/dresses-women/pl/3j3?page=',
            'https://www.meesho.com/shorts-women/pl/3kp?page=','https://www.meesho.com/trousers-men/pl/3lw?page=',
            'https://www.meesho.com/jeans-men/pl/3nw?page=','https://www.meesho.com/tshirts-men/pl/3k8?page=',
            'https://www.meesho.com/shirts-men/pl/3jq?page=','https://www.meesho.com/sports-shoes-men/pl/3kj?page=',
            'https://www.meesho.com/formal-shoes-for-men/pl/3o6?page=']
url_num=0
product_name = []
product_urls = []
product_id = []
main_product=[]
num=0
while(True):
    url = url_list[url_num]+str(page_number)
    driver.get(url)

    time.sleep(1)

    # Check if the page contains the Cloudflare challenge
    if 'Just a moment' in driver.page_source:
        # Wait for the challenge to complete (adjust the sleep time as needed)
        time.sleep(5)

    

    # Get the page source after dynamic content is generated
    html = driver.page_source

    # Create a BeautifulSoup object from the fetched HTML
    soup = BeautifulSoup(html, 'html.parser')
    

    required1 = soup.find('script',id='__NEXT_DATA__').prettify()


   
    s = str(required1)

    r = s.split('>\n')
    r = r[1].split('<')


    # Extract the JSON-LD script from the HTML
    json_ld_script = required1

    # Extract the JSON data from the script tag
    json_ld_data = json.loads(r[0])

    
    
    json_data = json.dumps(json_ld_data, indent=4)

   

 
    product = json_ld_data['props']['pageProps']['initialState']['productListing']['listing']['products']
    # print(product)
    for i in range(len(product)):
        
        for j in range(len(product[i]['products'])):
            
            # print(product[i]['products'][j]['full_details'].split("\n"))
            # product_urls.append(product[i]['products'][j]['consumer_share_text'].split('\n')[1])
            # product_name.append(product[i]['products'][j]['name'])
            ind = -1
            t = product[i]['products'][j]['full_details'].split('\n')
            #   print(t)
            sol = product[i]['products'][j]['name']+" "
            for k in range(len(t)):
                if t[k].split(': ')[0] == 'Fabric':
                      
                  sol+=t[k].split(': ')[1]
                  break
            
            if sol not in product_id:
            #   print(product[i]['products'][j]['full_details'].split('\n')[0].split(': '))
            #   ind = -1
            #   t = product[i]['products'][j]['full_details'].split('\n')
            # #   print(t)
            #   sol = product[i]['products'][j]['name']+" "
            #   for k in range(len(t)):
            #       if t[k].split(': ')[0] == 'Fabric':
                      
            #           sol+=t[k].split(': ')[1]
            #           break
              
            #   print(t[ind])
            # if(product[i]['products'][j]['consumer_share_text'].split('\n')[1] not in product_urls):
              main_product.append({'id':product[i]['products'][j]['id'],
                                   'vector':product[i]['products'][j]['consumer_share_text'].split('\n')[1],
                                   'name':product[i]['products'][j]['name'],
                                   'price':product[i]['products'][j]['min_product_price'],
                                   
                                #    'rating':product[i]['products'][j]['catalog_reviews_summary']['average_rating'],
                                   'description':sol
                                   
                                   })
              product_id.append(sol)
            #   product_urls.append(product[i]['products'][j]['consumer_share_text'].split('\n')[1])
            #   product_name.append(product[i]['products'][j]['name'])
              num+=1
            
            # if product[i]['products'][j]['id'] not in product_id:
            # #   print(product[i]['products'][j]['full_details'].split('\n')[0].split(': '))
            #   ind = -1
            #   t = product[i]['products'][j]['full_details'].split('\n')
            # #   print(t)
            #   sol = product[i]['products'][j]['name']+" "
            #   for k in range(len(t)):
            #       if t[k].split(': ')[0] == 'Fabric':
                      
            #           sol+=t[k].split(': ')[1]
            #           break
              
            # #   print(t[ind])
            # # if(product[i]['products'][j]['consumer_share_text'].split('\n')[1] not in product_urls):
            #   main_product.append({'id':product[i]['products'][j]['id'],
            #                        'vector':product[i]['products'][j]['consumer_share_text'].split('\n')[1],
            #                        'name':product[i]['products'][j]['name'],
            #                        'price':product[i]['products'][j]['min_product_price'],
                                   
            #                     #    'rating':product[i]['products'][j]['catalog_reviews_summary']['average_rating'],
            #                        'description':sol
                                   
            #                        })
            #   product_id.append(product[i]['products'][j]['id'])
            # #   product_urls.append(product[i]['products'][j]['consumer_share_text'].split('\n')[1])
            # #   product_name.append(product[i]['products'][j]['name'])
            #   num+=1
              
            
          
        # print(product[i]['page'],len(product[i]['products']),sep=" ")
            
    page_number += 1
        
        # Check if there is a next page, or exit the loop if not
    WebDriverWait(driver,1)
    time.sleep(1)

    # print(len(product_urls),num,sep=" ")
    if page_number>6:
        url_num+=1
        page_number = 1
        # print(len(product_urls))
        
        
    if url_num == len(url_list):
        break



driver.quit()

replacements = {
    "t-shirt": "tshirt",
    "t-shirts": "tshirt",
    "tee": "tshirt",
    "man": "men",
    "woman": "women",
    "(" : "",
    ")" : "",
    "  ": " "

}

stemmer = PorterStemmer()

# Lemmatiation
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text))

# Text preprocessing
def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()

    #Replace specific words
    for i, j in replacements.items():
        text = text.replace(i, j)

    # Tokenize the text
    tokens = nltk.word_tokenize(text)
    tokens = list(set(tokens))

    # Remove special characters and numbers
    tokens = [token for token in tokens if token.isalpha()]

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    #Normalize tokens
    tokens = [lemmatize_stemming(token) for token in tokens]
        
    # Return the preprocessed tokens as a list
    return ' '.join(tokens)

df = pd.DataFrame(main_product)

# Drop NULL Rows
df = df.dropna()

df["clean_text"] = df["description"].apply(lambda x: preprocess_text(x))

df
# d = {'id':product_name, "vector":product_urls}


df.to_csv('result.csv', index=False)



