import os
import boto3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def lambda_handler(event, context):
    try:
        user_id = event['body']['user_id']
        password = event['body']['password']
        nombre_tabla = os.environ['TABLE_USER']

        if user_id and password:
            hashed_password = hash_password(password)
            dynamodb = boto3.resource('dynamodb')
            t_usuarios = dynamodb.Table(nombre_tabla)
            t_usuarios.put_item(
                Item={
                    'user_id': user_id,
                    'password': hashed_password,
                }
            )
            mensaje = {
                'message': 'User registered successfully',
                'user_id': user_id
            }
            return {
                'statusCode': 200,
                'body': mensaje
            }
        else:
            mensaje = {
                'error': 'Invalid request body: missing user_id or password'
            }
            return {
                'statusCode': 400,
                'body': mensaje
            }

    except Exception as e:
        print("Exception:", str(e))
        mensaje = {
            'error': str(e)
        }
        return {
            'statusCode': 500,
            'body': mensaje
        }