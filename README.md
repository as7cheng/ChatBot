A Web-version Concierge ChatBot deployed on Amazon AWS.

URL: http://diningrobot.s3-website-us-east-1.amazonaws.com/

Tech-stack:
Languages: HTML/CSS, JS, Python

Platform: Amazon AWS

Services: S3, API Gateway, Lambda, SQS, LEX, DynamoDB, Elasticsearch, SNS, SES, CloudWatch
API: Yelp Fusion
WebUI: Provided by course.

It is a chatbot that gives users restaurant suggestions based on users' input,  supports users to type in some information e.g. cuisine type, location, number of people and date, etc., and returns users an email or text-message contains some restaurant suggestions with details.
NOTE: since the limited space of AWS free-tier, currently it only has about 5,000 restaurants' information located around NYC. Also, due to the unreliability of SNS, I chose the SES as a demo.

Development process:
1. Deploy the frontend part(assets) on S3
2. Import 
