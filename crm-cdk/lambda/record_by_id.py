import os
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    method = event['httpMethod']
    record_id = event['pathParameters']['id']

    if method == 'GET':
        try:
            response = table.get_item(Key={'id': record_id})
            item = response.get('Item')
            if not item:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Record not found'})
                }
            return {
                'statusCode': 200,
                'body': json.dumps(item)
            }
        except Exception as e:
            return _error_response(str(e))

    elif method == 'PUT':
        try:
            body = json.loads(event['body'])

            update_expr = """
                SET first_name=:f, last_name=:l, email=:e,
                    phone=:p, address=:a, city=:c,
                    province=:pr, country=:co
            """
            expr_values = {
                ':f': body['first_name'],
                ':l': body['last_name'],
                ':e': body['email'],
                ':p': body['phone'],
                ':a': body['address'],
                ':c': body['city'],
                ':pr': body['province'],
                ':co': body['country'],
            }

            table.update_item(
                Key={'id': record_id},
                UpdateExpression=update_expr,
                ExpressionAttributeValues=expr_values
            )

            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Record updated successfully'})
            }

        except Exception as e:
            return _error_response(str(e))

    elif method == 'DELETE':
        try:
            table.delete_item(Key={'id': record_id})
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Record deleted successfully'})
            }
        except Exception as e:
            return _error_response(str(e))

    return {
        'statusCode': 405,
        'body': json.dumps({'error': f'Method {method} not allowed'})
    }

def _error_response(message):
    return {
        'statusCode': 500,
        'body': json.dumps({'error': message})
    }
