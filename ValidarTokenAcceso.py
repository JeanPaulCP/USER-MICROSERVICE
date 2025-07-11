import os
import boto3
from datetime import datetime
import json

def lambda_handler(event, context):
    print(event) 
    tenant_id = event['body']['tenant_id']
    token = event['body']['token']  
    tabla_token = os.environ['TABLE_NAME_TOKENS']

    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tabla_token)

    response = table.get_item(
    Key={
        'tenant_id': tenant_id,
        'token': token
        }
    )

    if 'Item' not in response:
        return {
            'statusCode': 403,
            'body': 'Token no existe'
        }
    else:
        expires = response['Item']['expires']
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if now > expires:
            return {
                'statusCode': 403,
                'body': 'Token expirado'
            }

    # Salida (json)
    return {
        'statusCode': 200,
        'body': 'Token valido'
    }
