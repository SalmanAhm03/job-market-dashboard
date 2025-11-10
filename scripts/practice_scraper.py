import requests
from bs4 import BeautifulSoup

def scrape_quotes():
    url = "http://quotes.toscrape.com/"
    
    print("Fetching quotes website...")
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Success! Status Code: {response.status_code}\n")

        soup = BeautifulSoup(response.text, 'lxml')
        
        quotes = soup.find_all('div', class_='quote')
        
        print(f"Found {len(quotes)} quotes:\n")
        
        for i, quote in enumerate(quotes[:5], 1):
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            
            print(f"Quote {i}:")
            print(f"  Text: {text}")
            print(f"  Author: {author}\n") 
         
        return True
    else:
        print(f"Failled. Status Code: {response.status_code}")
        return False
    
if __name__ == "__main__":
    scrape_quotes()

