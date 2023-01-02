import json
from typing import List

import boto3


def encode_record(record: dict):
    return str(record).encode('utf-8')


stream_name = "PUT-S3-ulaFO"
client = boto3.client("firehose")

with open("../data/2022-11-29_ec812e23-91a0-4da2-9b12-ae2ad108779a.json") as file:
    data: List[dict] = json.load(file)

# encode records
data_encoded = [{"Data": encode_record(record)} for record in data]

response = client.put_record_batch(
    DeliveryStreamName=stream_name,
    Records=data_encoded
)