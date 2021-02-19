from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3


host = "search-restaurantsearch-pg7ixoc7a5rq3l2i7qpopa67zq.us-east-1.es.amazonaws.com"
region = 'us-east-1'

service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)


es = Elasticsearch(
    hosts = [{'host': host, 'port': 443}],
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('yelp-restaurants')

scan = table.scan()
count = 1
    #headers = {'Content-Type' : 'application/json'} # copy from curl


for item in scan["Items"]:
    data = {
        "id" : item["businessID"],
        "type" : item["category"]
    }
    es.index(index="restaurants", doc_type="Restaurant", id = count, body=data)
    print(count)
    count += 1