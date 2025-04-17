import os

import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(url):
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params={
            "apikey":os.getenv('SCRAPE_KEY'),
            "linkedInUrl":url
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10
        )
        data = response.json().get("person")
        return data

# print(scrape_linkedin_profile(url="https://de.linkedin.com/in/sebastian-f-konrad"))
