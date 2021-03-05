from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
import time
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


table = dynamodb.Table('yelp-restaurants')
# while table.table_status != 'ACTIVE':
#     table.reload()

json_file = "../RestData/businesses_dynamo_1.json"
businesses = json.load(open(json_file, "r"), parse_float = decimal.Decimal)
count = len(businesses)
i = 0
for buz in businesses:
    item = dict(
        insertedAtTimestamp = time.asctime(time.localtime(time.time())),
        business_id = buz['id'],
        name = buz['name'],
        category = buz['category'],
        address = buz['address'],
        coordinates = buz['coordinates'],
        review_count = buz['review_count'],
        rating = buz['rating'],
        zip_code = buz['zip_code']
    )
    table.put_item(Item=item)
    time.sleep(0.75)
    i += 1
    #if i % 100 == 0:
    print("{}/{} items added...".format(i, count))

