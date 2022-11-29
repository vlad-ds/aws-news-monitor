import os
import datetime

import requests as requests
from dotenv import load_dotenv

from logger import log

# load environment variables from .env file if present
load_dotenv()

API_KEY = os.environ.get("API_KEY")

log.info("Retrieved API KEY of length %s" % len(API_KEY))

endpoint = 'https://newsapi.org/v2/everything'
query = "apple OR microsoft OR alphabet OR Amazon OR meta"
today_iso: str = datetime.date.today().isoformat()

params = {'apiKey': API_KEY,
          'qInTitle': query,
          'from': today_iso
          }

resp = requests.get(endpoint, params)

if resp.status_code == 200:
    log.info("Request was successful.")

data = resp.json()
n_articles = data['totalResults']

if n_articles:
    log.info("Extracted %i articles" % n_articles)

filename = f"{today_iso}.json"