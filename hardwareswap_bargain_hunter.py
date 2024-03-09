import requests
from bs4 import BeautifulSoup
import re
import praw

reddit = praw.Reddit(client_id='lIkftPNxPIEUWnge7Hg5cQ',
                     client_secret='HJBah6bCX8ZW-pnTyTAXV-xVvduH0w',
                     user_agent='hardwareswap_scrapper')

def scrape_amazon_product(item_name):
    # Send HTTP GET request to the product page
    product_url = f"https://www.amazon.com/s?k={item_name}"
    response = requests.get(product_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract product title
        title_element = soup.find('span', {'id': 'productTitle'})
        title = title_element.text.strip() if title_element else 'Title not found'
       
        
        # Extract product price
        price_element_whole = soup.find('span', {'class': 'a-price-whole'})
        price_element_fraction = soup.find('span', {'class': 'a-price-fraction'})
        price_1 = price_element_whole.text.strip().rstrip('.') if price_element_whole else 'Price not found'
        price_2 = price_element_fraction.text.strip().rstrip('.')
        
        return {'title': title, 'price': price_1 +'.'+ price_2 }
    else:
        print('Failed to retrieve Amazon search results:', response.status_code)
        return None

def reddit_scrap():
    subreddit = reddit.subreddit('hardwareswap')
    for post in subreddit.new(limit=10):
        print('-------------------')
        print(post.title)
        print(post.url)
        print(post.score)
        print('-------------------')
        title = str(post.title)
        found = re.search(r'\[H\](.*?)\[W\]', title)
        if found:
            item_name = found.group(1).strip()
            print(item_name)
        else:
            print('No item found')
        
        items_name = scrape_amazon_product(item_name)

        if items_name:
            for i, result in enumerate(amazon_results, start=1):
                print(f"Result {i}:")
                print("Title:", result['title'])
                print("Price:", result['price'])
                print("URL:", result['url'])
                print("---")

reddit_scrap()
# Example usage
#amazon_url = 'https://www.amazon.com/MSI-RTX-4060-Architecture-2X/dp/B0C8BPW1SP/ref=sr_1_1?crid=BZ9RHZY1F828&dib=eyJ2IjoiMSJ9.Sxa1Ys6Cd91ocwPjOEIoYYRt1I49F5t7Rzm4Me15n-IZVO2n2nTSrCGfg-eTUNZC2z4DVK4FW-x_P8gsPfsyFRxAH0p9JY4oXcrbanAxvF1ge4Jg71LuVL-Vo9tatVx801BE5EIgZGQPEW4bcXp7N6G8ApxcaE6Dv8_FhM-VcvrAYve_r5HyTZMD02vckWeRIJ8ZBBsyumgMeZQkGRLgpFsdbm-rRk5fUaW4Olcfde0.H0ApxlGWNusWhT-OC2psnmdsv-dKVVDg719w7ooSbmw&dib_tag=se&keywords=rtx&qid=1710017710&sprefix=rt%2Caps%2C134&sr=8-1'
#product_data = scrape_amazon_product(amazon_url)
#on_amazon_price = product_data['price']
#if product_data:
#    print('Product Title:', product_data['title'])
#    print('Product Price:', product_data['price'])
