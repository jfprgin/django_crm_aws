import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    body = json.loads(event['body'])

    item = {
        "id": str(uuid.uuid4()),
        "first_name": body["first_name"],
        "last_name": body["last_name"],
        "email": body["email"],
        "phone": body["phone"],
        "address": body["address"],
        "city": body["city"],
        "province": body["province"],
        "country": body["country"],
    }

    table.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps({"message": "Saved successfully!", "id": item["id"]})
    }
