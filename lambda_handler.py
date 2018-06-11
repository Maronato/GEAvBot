import json
from senpaibot.core import receiver, send_subscriptions


print('Loading function')


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def test_response(payload):
    return respond(None, {'status': 'success'})


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'POST': receiver,
        'SUB_UPDATE': send_subscriptions
    }

    test_operations = {
        'GET': test_response
    }

    if event.get('httpMethod', False):
        operation = event['httpMethod']
    else:
        operation = "not available"

    try:
        pay = json.loads(event['body'])
    except TypeError:
        pay = event['body']

    if operation in operations:
        payload = event['queryStringParameters'] if operation == 'GET' else pay
        return respond(None, operations[operation](payload))
    elif operation in test_operations:
        payload = event['queryStringParameters'] if operation == 'GET' else pay
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))
