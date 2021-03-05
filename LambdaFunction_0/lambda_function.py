import json
import boto3
def lambda_handler(event, context):
    
    # print(event)
    # a = event['messages']
    # print(a[0]['unstructured']['text'])

    # tExt = json.loads(event['messages'])['type']['unstructured']['text']
    reText = event['messages'][0]['unstructured']['text']

    client=boto3.client('lex-runtime')
    response = client.post_text(
        botName = 'DiningConciergeChatBot',
        botAlias = 'DCCB',
        userId='kwy',
        inputText=reText,
        )
    
    message = response['message']

    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        
        # 'messages': [{
        #     'type': 'unstructured',
        #     'unstructured': {
        #         'text': 'I am still under development. Please come back later.'
        #     }
        # }],

        'messages': [{
            'type': 'unstructured',
            'unstructured': {
                'text': message
            }
        }],
        
        'body': json.dumps(message)
    }