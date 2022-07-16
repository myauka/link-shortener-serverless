import os
import json
import time
import boto3
import random
import string

dynamodb_client = boto3.client("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
DNS_RECORD = os.environ["DNS_RECORD"]


def add_short_url(event, context):
    body = event["body"]

    if not body:
        return {"statusCode": 400, "body": json.dumps(
            {"error": "body is empty"})
        }

    request_body = json.loads(body)

    long_url = request_body.get("long-url")
    if not body:
        return {"statusCode": 400, "body": json.dumps(
            {"error": "link was not received. param long-url required"})
        }

    url_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

    exp_date = f'{int(time.time()) + 60}'

    dynamodb_client.put_item(
        TableName=TABLE_NAME,
        Item={
            "url_id": {"S": url_id},
            "long_url": {"S": long_url},
            "ttl": {"N": exp_date}
        }
    )

    short_url = DNS_RECORD + "link/" + url_id

    return {
        "statusCode": 200,
        "body": json.dumps({
            "url_id": url_id,
            "short_url": short_url,
            "ttl": exp_date
        })
    }
