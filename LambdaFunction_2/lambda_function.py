from receiveMessage import fromSqs
from searchES import searchES
import boto3
from boto3.dynamodb.conditions import Key, Attr
import re
class Lambda2():
    def __init__(self):
        pass
        
    def fromSqs(self):
        fro = fromSqs()
        msg = fro.receive_func()
        return msg
    
    def searchES(self, cuisine_type, num_restaurants):
        """Query Elasticsearch index for restaurants in given cuisine type. 
        :param cuisine_type: the category of restaurants you want to search for
                             Supported inputs: ['American', 'Chinese', 'Japanese', 'Italian', 'Mexican', 'Indian', 'Thai']
        :param num_restaurants: number of results to get
        z
        :return hits: list of restaurants in cuisine type. 

        """
        index_name = 'restaurants'
        s = searchES(index_name)
        hits = s.search_es(cuisine_type, num_restaurants)
        return hits
        
    def searchDynamo(self, restaurant_id): 
        """Query DynamoDB for restaurant details using restaurant_id. 
        :param restaurant_id: business ID of the restaurant as a string. 
                              Example: 'Rc1lxc5lSKJYd162JHNMfQ'
        
        :return item: restaurant details stored in Dynamo. 
                      Example: [{'business_id': 'qgY41g_eg0eNzewCXmKcaA', 'rating': Decimal('5'), ...}]
                      Headers: ['business_id', 'rating', 'zip_code', 'insertedAtTimestamp', 'category', 'address', 'name', 'review_count', 'coordinates']
        """
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('yelp-restaurants')
        response = table.scan(
                FilterExpression=Attr('business_id').eq(restaurant_id)
            )
        item = response['Items']
        return item
        
    def toSES(self, msg, email_address):
        AWS_REGION = "us-east-1"
        SUBJECT = "Dinning Suggestion"

        CHARSET = "UTF-8"
        SENDER = "Dinning Suggestion <wk2359@columbia.edu>"
        RECIPIENT = email_address
        client = boto3.client('ses', region_name=AWS_REGION)
        BODY_TEXT = (msg)
        client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

def lambda_handler(event, context):
    lf2 = Lambda2()
    msg = lf2.fromSqs()
    cuisine = None
    rest_info = None
    
    if 'Body' in msg:
        msg_intent = msg['Body']
        cuisine = re.findall(r'Cuisine:(.*)N',msg_intent)[0]
        numberofPeople = re.findall(r'Numberofpeople:(.*)D',msg_intent)[0]
        dining_time = re.findall(r'Time:(.*)E',msg_intent)[0]
        date = re.findall(r'Date:(.*)T',msg_intent)[0]
        email_address = re.findall(r'Email_address:(.*)',msg_intent)[0]

    if cuisine:
        restaurants = lf2.searchES(cuisine_type=cuisine, num_restaurants=3)
        # print(restaurants)
        rest_info = []
        for restaurant in restaurants:
            rest_info.append(lf2.searchDynamo(restaurant['restaurant_id'])[0])

    if rest_info:
        msg_SES = "Thanks, Here are my {} restaurant suggestions for {} people, for dining at {} on {}: \
        \n  - {} located at {}; \n  - {} located at {}; \n  - {} located at {}. \
        Enjoy your meal!".format(cuisine, numberofPeople, dining_time, date, rest_info[0]['name'], rest_info[0]['address'],
        rest_info[1]['name'], rest_info[1]['address'],rest_info[2]['name'], rest_info[2]['address'])
        lf2.toSES(msg_SES, email_address)
    
    
if __name__ == "__main__":
    lambda_handler(None, None) 
    

