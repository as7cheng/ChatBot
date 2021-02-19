import boto3
from datetime import date
import json
import requests
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    #
    # SQS part
    #

    # Get SQS
    queue_url = "https://sqs.us-east-1.amazonaws.com/452853680688/user-info"
    sqs = boto3.client('sqs')

    # Pull message form SQS
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=['SentTimestamp'],
        MaxNumberOfMessages=1,
        MessageAttributeNames=['All'],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    
    if "Messages" not in response.keys():
        return "Please try later"
 
    
    message = response['Messages'][0]
    # Get the receipt handle for deleting message later
    receipt_handle = message['ReceiptHandle']
    

    # Pick up the user's input
    data = json.loads(message['Body'])
    
    # Generate the information from usr's input
    cuisine = data['Cuisine'].strip()
    num_of_people = data['Amount'].strip()
    # If user needs the day is today, show today
    if (data['Date'] == str(date.today())):
        day = 'today'
    else:
        day = data['Date']
    time = data['Time']
    phone = data['PhoneNumber'].strip()

  
    
    #
    # ElasticSearch part
    #
    
    # Hold partial of the return meassge to user
    reply_sns = f'Hello! Here are my {cuisine} resraurant suggestions for {num_of_people} people, for {day} at {time}: '
    print (reply_sns)
    
    # Prepare for doing search on the ElasticSearch
    ENDPOINT = "https://search-restaurantsearch-pg7ixoc7a5rq3l2i7qpopa67zq.us-east-1.es.amazonaws.com/restaurants/Restaurant"
    es_query = ENDPOINT + "/_search?size=3&&q=type: " + cuisine
    headers = {'Content-Type' : 'application/json'}
    # Get the result searched based on user's chosen cuisine type
    es_response = requests.get(es_query, headers=headers, auth=("YOUR MASTER NAME", "MASTER PASSWOED")).json()
    print(es_response)
    
    # Pick up the data
    es_data = es_response['hits']['hits']
    # Store the business id for the restaurants
    es_ids = []
    for data in es_data:
        es_ids.append(data["_source"]["id"])

    
    #
    # DynamoDB part
    #
    
    # Get the table we store the information of restaurants
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    
    # Index as the number before each retaurant in the message sent back to the user
    index = 1
    for es_id in es_ids:
        # For each id got from ElasticSearch, find them in the table
        response = table.query(
            KeyConditionExpression=Key('businessID').eq(es_id)
        )
        # In case the response is nothing
        if response != []:
        # Pick up the information of the restaurant
            item = response['Items'][0]
            reply_sns += str(index) + '.' + item['name'] + ', located at' + item['address'] + '. '
            index += 1        
    reply_sns += 'Enjoy your meal!'
    
    
    #
    # SES Part
    #
    
    # Create a new SES resource
    client = boto3.client('ses')
    # Default sender and recipient for testing
    SENDER = "s7primes@gmail.com"
    RECIPIENT = "shihan.cheng@columbia.edu"
    # Email subject
    SUBJECT = "Your Restaurant Suggestions Are Here!"
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': reply_sns,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
        # Delete received message from queue
        sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
        )
    

        
        

