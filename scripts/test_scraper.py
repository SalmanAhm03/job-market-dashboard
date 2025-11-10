import requests
from bs4 import BeautifulSoup
import time

# URL of the webpage to scrape
url = "https://www.indeed.com/jobs?q=data+analyst&l=United+States"

# Headers to make our request look more like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# Send a GET request to the webpage
print("Fetching the webpage...")
response = requests.get(url, headers = headers, timeout = 10)

# Print the status code of the response
print(f"Status Code: {response.status_code}")

# Check if the request was successful
if response.status_code == 200:
    print("Success! Webpage fetched.")
    print(f"Page size: {len(response.text)} characters")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find the page title for testing
    page_title = soup.find('title')
    print(f"Page Title: {page_title.text if page_title else 'No title found'}")
else:
    print(f"Failed to fetch webpage. Status code: {response.status_code}")


