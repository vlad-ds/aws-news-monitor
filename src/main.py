import json
import os
import datetime
import uuid
import random

import requests as requests
from dotenv import load_dotenv

from logger import log

# load environment variables from .env file if present
load_dotenv()
API_KEY = os.environ.get("API_KEY")
log.info("Retrieved API KEY of length %s" % len(API_KEY))


def get_sample(sample_size: int = 5):

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
    else:
        log.error("Request failed!")
        log.info(resp)
        return

    data = resp.json()
    n_articles = data['totalResults']

    if n_articles:
        log.info("Extracted %i articles" % n_articles)
    else:
        log.error("Request returned 0 articles")
        return

    articles = random.sample(data['articles'], sample_size)

    filename = f"{today_iso}_{uuid.uuid4()}.json"
    dump_path = f"../data/{filename}"

    with open(dump_path, 'w') as file:
        json.dump(articles, file)

    log.info("Saved %i articles at %s" % (sample_size, dump_path))


if __name__ == "__main__":
    get_sample()
