import boto3
import hashlib
import uuid
import os
from datetime import datetime, timedelta

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    # Entrada (json)
    user_id = event['body']['user_id']
    password = event['body']['password']
    tabla_usuarios = os.environ['TABLE_USER']
    tabla_token = os.environ['TABLE_TOKEN']
    hashed_password = hash_password(password)
    # Proceso
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tabla_usuarios)
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' not in response:
        return {
            'statusCode': 403,
            'body': 'Usuario no existe'
        }
    else:
        hashed_password_bd = response['Item']['password']
        if hashed_password == hashed_password_bd:
            # Genera token
            token = str(uuid.uuid4())
            fecha_hora_exp = datetime.now() + timedelta(minutes=60)
            registro = {
                'token': token,
                'expires': fecha_hora_exp.strftime('%Y-%m-%d %H:%M:%S')
            }
            table = dynamodb.Table(tabla_token)
            dynamodbResponse = table.put_item(Item=registro)
        else:
            return {
                'statusCode': 403,
                'body': 'Password incorrecto'
            }

    # Salida (json)
    return {
        'statusCode': 200,
        'token': token
    }
