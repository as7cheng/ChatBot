import boto3
import requests
import json
import datetime
from decimal import Decimal
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

api_key = 'GSJaayM2a9BAEbDOlm5Goc7m_vlbAFY3zYaJStmDRxiHeAW0cpMt3KBNLAX9OwRU-QTKe0twzx3azaH-d7W5YyZJfUWfd1jlEwuUUC-LQiuNxZNVM7_pp9zmkUkrYHYx'
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % api_key}


cuisines = ['seafood'] #'american', chinese', 'japanese', 'seafood', 'mexican', 'italian', 'french', 'korean'

for cuisine in cuisines:
    for i in range(25):
        PARAMETERS = {
            'term': 'restaurant',
            'location': 'New york',
            'radius': 40000,
            'categories': cuisine,
            'limit': 50,
            'offset': 50 * i,
            'sort_by': 'best_match'
        }

        response = requests.get(url, params=PARAMETERS, headers=headers)
        data = response.json()

        for business in data['businesses']:
            try:
                table.put_item(
                    Item={
                        'businessID': business['id'],
                        'name': business['name'],
                        'category': cuisine,
                        'address': business['location']['address1'],
                        'latitude': Decimal(str(business['coordinates']['latitude'])),
                        'longitude': Decimal(str(business['coordinates']['longitude'])),
                        'reviewCount': business['review_count'],
                        'rating': Decimal(str(business['rating'])),
                        'zipcode': business['location']['zip_code'],
                        'insertedAtTimestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                    ConditionExpression='attribute_not_exists(businessID)'
                )
            except ClientError as e:
                print(e.response['Error']['Code'])