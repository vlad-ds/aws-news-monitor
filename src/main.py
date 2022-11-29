import json
import os
import datetime
import uuid
import random

import requests as requests
from dotenv import load_dotenv

from logger import log


def get_sample(api_key: str,
               sample_size: int = 5):

    endpoint = 'https://newsapi.org/v2/everything'
    query = "apple OR microsoft OR alphabet OR Amazon OR meta"
    today_iso: str = datetime.date.today().isoformat()

    params = {'apiKey': api_key,
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


def main():
    # load environment variables from .env file if present
    load_dotenv()
    api_key = os.environ.get("API_KEY")
    if api_key:
        log.info("Retrieved API KEY of length %s" % len(api_key))
    else:
        log.error("API key not found! Exiting.")
        return
    get_sample(api_key)


if __name__ == "__main__":
    main()
