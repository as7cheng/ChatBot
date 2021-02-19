A Web-version Concierge ChatBot deployed on Amazon AWS.

URL: http://diningrobot.s3-website-us-east-1.amazonaws.com/

Tech-stack:
1. Languages: HTML/CSS, JS, Python.
2. Services: S3, API Gateway, Lambda, SQS, LEX, DynamoDB, Elasticsearch, SNS, SES, CloudWatch.
3. API: Yelp Fusion.
4. WebUI: Provided by course.

It is a chatbot that gives users restaurant suggestions based on users' input,  supports users to type in some information e.g. cuisine type, location, number of people and date, etc., and returns users an email or text-message contains some restaurant suggestions with details.
NOTE: Since the limited space of AWS free-tier, currently it only has about 5,000 restaurants' information located around NYC. Also, due to the unreliability of SNS, I chose the SES as a demo.

Important: Remember to create exexution roles and attached neccessary policies for each part through IAM
Development process:
1. Deploy the frontend part(assets) on S3
2. Import aics-swagger.yaml into API Gateway, generate new SDK and replace the it with the old version in assets. Remember to enable CORS for your API before doing so.
3. Create Lambda function LF0 to connect API Gateway. It works as:
5. Create a new bot using the Amazon Lex service.
6. Create a Lambda function (LF1) and use it as a code hook for Lex, which essentially entails the invocation of your Lambda before Lex responds to any of your requests.
7. Modify your LF0, it works as when the API receives a request, you should 1. extract the text message from the API request, 2. send it to your Lex chatbot, 3. wait for the response, 4. send back the response from Lex as the API response.
8. Use the Yelp API to collect 5,000+ random restaurants from the city you like.
9. Create a DynamoDB table and named “yelp-restaurants”, storethe restaurants you scrape, in DynamoDB. Here, you have two ways to do so. One is to write a helper function scape the restaurants information through Yelp fusion and in the same function use boto3 to store them in the DynamoDB, the function has been attached in the Helper folder. Another one is to modify the helper function and save the result you scraped as a JSON file. Then write a simple function to upload it to DynamoDB.
10. Create an ElasticSearch, an index called “restaurants” and an ElasticSearch type under the index “restaurants” called “Restaurant”. Store partial information for each restaurant scraped in ElasticSearch under the “restaurants” index, where each entry has a “Restaurant” data type.
11. Build a suggestions module, that is decoupled from the Lex chatbot. For doing this step, Create a new Lambda function (LF2) that acts as a queue worker. Whenever it is invoked it 1. pulls a message from the SQS queue (Q1), 2. gets a random restaurant recommendation for the cuisine collected through conversation from ElasticSearch and DynamoDB, 3. formats them and 4. sends them over text message to the phone number included in the SQS message, using SNS or SES.
12. Set up a CloudWatch event trigger that runs every minute and invokes the Lambda function as a result.
