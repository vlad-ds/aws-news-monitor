import json
import os
import datetime
import uuid
import random

import requests as requests
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

from logger import log


def get_aws_secret():

    secret_name = "news_api_key"
    region_name = "eu-central-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']

    # Your code goes here.

    return secret


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


def main(secret_source: str = "aws"):

    api_key = None

    if secret_source == "aws":
        api_key = get_aws_secret()
    elif secret_source == "env":
        load_dotenv()
        api_key = os.environ.get("NEWS_API_KEY")
    else:
        log.error("secret_source arg must be either 'aws' or 'env'!")

    if api_key:
        log.info("Retrieved API KEY of length %s" % len(api_key))
    else:
        log.error("API key not found! Exiting.")
        return

    get_sample(api_key)


if __name__ == "__main__":
    main()
