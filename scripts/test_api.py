# Import required libraries
import requests  # For making HTTP requests to APIs
import os  # For accessing environment variables
from dotenv import load_dotenv  # For loading .env file
import json  # For pretty-printing JSON data
import time  # For adding delays between retries

# Load environment variables from .env file
# This reads the .env file and makes the variables available via os.getenv()
load_dotenv()

# Get the API key from environment variables
# This keeps our key secure and out of the code
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

# Check if we successfully loaded the API key
if not RAPIDAPI_KEY:
    print("ERROR: API key not found! Check your .env file.")
    exit()

print("API key successfully loaded from .env file.")
print(f"API key starts with: {RAPIDAPI_KEY[:10]}...")  # Show first 10 chars only for security

# The API endpoint URL
# This is the specific URL that the JSearch API uses for job searches
url = "https://jsearch.p.rapidapi.com/search"

# Query parameters - what we're searching for
# These are sent to the API to specify what data we want
querystring = {
    "query": "data analyst in USA",  # What job and where
    "page": "1",  # Which page of results (pagination)
    "num_pages": "1"  # How many pages to return
}

# Headers - additional information sent with the request
# These tell the API who we are and what format we want
headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,  # Our authentication key
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"  # Which API we're calling
}

# Make the API request with retry logic
print("\nFetching job data from JSearch API...")
print(f"Searching for: {querystring['query']}\n")

# We'll try up to 3 times if there's a timeout
max_retries = 3
retry_count = 0

# Keep trying until we succeed or run out of retries
while retry_count < max_retries:
    try:
        # Attempt number (1, 2, or 3)
        attempt = retry_count + 1
        print(f"Attempt {attempt}/{max_retries}...")
        
        # Send GET request to the API
        # timeout=30 means wait max 30 seconds for a response (increased from 10)
        response = requests.get(url, headers=headers, params=querystring, timeout=30)
        
        # If we get here, the request succeeded (no timeout)
        # Check if the request was successful
        # Status code 200 means "OK" - the request worked
        if response.status_code == 200:
            print(f"✓ Success! Status code: {response.status_code}")
            
            # Parse the JSON response
            # .json() converts the response text into a Python dictionary
            data = response.json()
            
            # Print some basic info about what we got
            print(f"✓ Received data from API")
            print(f"✓ Number of jobs found: {len(data.get('data', []))}")
            
            # Print the first job to see the structure
            if data.get('data') and len(data['data']) > 0:
                print("\n--- First Job Example ---")
                first_job = data['data'][0]
                
                # Pretty print the JSON so it's readable
                # indent=2 makes it nicely formatted with indentation
                print(json.dumps(first_job, indent=2))
                
                print("\n--- Key Information ---")
                print(f"Job Title: {first_job.get('job_title', 'N/A')}")
                print(f"Company: {first_job.get('employer_name', 'N/A')}")
                print(f"Location: {first_job.get('job_city', 'N/A')}, {first_job.get('job_state', 'N/A')}")
                print(f"Posted: {first_job.get('job_posted_at_datetime_utc', 'N/A')}")
            
            # Save the full response to a file for inspection
            with open('data/api_response_sample.json', 'w', encoding='utf-8') as f:
                # Write the JSON data to a file
                # indent=2 makes it readable, ensure_ascii=False preserves special characters
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print("\n✓ Full API response saved to: data/api_response_sample.json")
            
            # Exit the retry loop since we succeeded
            break
            
        else:
            # If status code is not 200, something went wrong
            print(f"✗ Failed! Status code: {response.status_code}")
            print(f"Error message: {response.text}")
            # Exit the retry loop since this is not a timeout issue
            break
    
    # Catch timeout errors specifically
    except requests.exceptions.Timeout:
        retry_count += 1
        print(f"✗ Request timed out (waited 30 seconds)")
        
        # If we have retries left, wait and try again
        if retry_count < max_retries:
            wait_time = 5  # Wait 5 seconds before retrying
            print(f"   Waiting {wait_time} seconds before retry...\n")
            time.sleep(wait_time)  # Pause execution for 5 seconds
        else:
            # We've used all our retries
            print(f"\n✗ Failed after {max_retries} attempts")
            print("   Possible causes:")
            print("   - Slow internet connection")
            print("   - API server is experiencing high traffic")
            print("   - Your API key might have rate limits")
            print("\n   Try again in a few minutes, or check your RapidAPI dashboard")
    
    # Catch any other network-related errors
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error: {e}")
        print("   Check your internet connection and try again")
        break  # Don't retry for general network errors
    
    # Catch any unexpected errors
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        break  # Don't retry for unexpected errors