import boto3
import json
import os
import read_config as rc

lambda_client = boto3.client('lambda')
COBOL_FUNCTION = os.environ["PROXY_COBOL_FUNCTION"]


def lambda_handler(event, context):
    respons_query = invole_cobol_lambda(event['body'])
    config_resgister = rc.find_register(respons_query['body'])
    result = mapping_response(config_resgister, respons_query['body'])

    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": "application/json"
        },
        'body': result
    }


def invole_cobol_lambda(body):
    response_cobol = lambda_client.invoke(
        FunctionName=COBOL_FUNCTION,
        InvocationType='RequestResponse',
        Payload=bytes(body, 'utf-8')
    )

    response_cobol = json.loads(
        response_cobol['Payload'].read().decode('utf-8'))

    return response_cobol


def mapping_response(config, data):
    maping_data = {'claves': []}
    position = 0

    while position < len(data) - config['longitud']:
        sub_data = data[position:position + config['longitud']]
        new_resgister = create_resgister(config['campos'], sub_data)
        maping_data['claves'].append(new_resgister)
        position += config['longitud']

    return json.dumps(maping_data)


def create_resgister(config_field, data):
    register = {}
    for campo in config_field:
        value = data[campo['posInicial'] - 1: campo['posFinal']].rstrip()
        register[campo['nombre']] = value

    return register
