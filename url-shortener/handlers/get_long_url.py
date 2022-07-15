import os
import json
import time
import boto3

dynamodb_client = boto3.client("dynamodb")

TABLE_NAME = os.environ["TABLE_NAME"]
DNS_RECORD = os.environ["DNS_RECORD"]


def redirect_to_long_url(event, context):
    url_id = event["pathParameters"]["url_id"]

    result = dynamodb_client.get_item(
        TableName=TABLE_NAME,
        Key={"url_id": {"S": url_id}}).get("Item")

    exp_date = result.get("ttl").get("N")
    print(f'Я ТУТ {exp_date}')

    if int(exp_date) < int(time.time()):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "link expired"})
        }

    if not result:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "link not found"})
        }

    long_url = result.get("long_url").get("S")

    return {
        "headers": {"Location": long_url},
        "statusCode": 301,
    }
