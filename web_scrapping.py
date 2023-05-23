from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

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
url_list = ['https://www.meesho.com/tops-ladies/pl/3ja?page=','https://www.meesho.com/women-clothing/pl/9om?page=',
            'https://www.meesho.com/women-clothing/pl/9om?page=','https://www.meesho.com/dresses-women/pl/3j3?page=',
            'https://www.meesho.com/shorts-women/pl/3kp?page=','https://www.meesho.com/trousers-men/pl/3lw?page=',
            'https://www.meesho.com/jeans-men/pl/3nw?page=','https://www.meesho.com/tshirts-men/pl/3k8?page=',
            'https://www.meesho.com/shirts-men/pl/3jq?page=','https://www.meesho.com/sports-shoes-men/pl/3kj?page=',
            'https://www.meesho.com/formal-shoes-for-men/pl/3o6?page=']
url_num=0
product_name = []
product_urls = []
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

    # Use BeautifulSoup to find and extract the desired information
    # You can navigate the HTML structure, find specific elements, and extract data using BeautifulSoup methods
    


    required1 = soup.find('script',id='__NEXT_DATA__').prettify()


    # print(required1)
    s = str(required1)

    r = s.split('>\n')
    r = r[1].split('<')


    # Extract the JSON-LD script from the HTML
    json_ld_script = required1

    # Extract the JSON data from the script tag
    json_ld_data = json.loads(r[0])

    
    # Convert the JSON-LD data to JSON format
    json_data = json.dumps(json_ld_data, indent=4)

    # Print the JSON data
    # print(json_data)

 
    product = json_ld_data['props']['pageProps']['initialState']['productListing']['listing']['products']

    for i in range(len(product)):
        print(i)
        # temp = product[i]['products']
        # print(temp)
        for j in range(len(product[i]['products'])):
            print(product[i]['products'][j]['consumer_share_text'].split('\n')[1])
            print(product[i]['products'][j]['name'])
            # print(product[i]['products'][j]['description'])
            print(product[i]['products'][j]['share_text'].split('\n'))
            if(product[i]['products'][j]['consumer_share_text'].split('\n')[1] not in product_urls):
              product_urls.append(product[i]['products'][j]['consumer_share_text'].split('\n')[1])
              product_name.append(product[i]['products'][j]['name'])
              
            
    page_number += 1
        
        # Check if there is a next page, or exit the loop if not
    WebDriverWait(driver,1)
    time.sleep(1)

    if page_number>10:
        url_num+=1
        page_number = 1

        
    if url_num == len(url_list):
        break



driver.quit()

d = {'id':product_name, "vector":product_urls}
df = pd.DataFrame(d)


df.to_csv('result.csv', index=False)


# we have to retrieve consumer_share_text for product url, name, description, share_text  

