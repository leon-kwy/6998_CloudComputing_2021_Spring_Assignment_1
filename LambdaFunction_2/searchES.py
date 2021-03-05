from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import json
import boto3
import random

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

HOST = "https://search-domainforchatbot-gg7624dwhmrjufczb5k7ewur2e.us-east-1.es.amazonaws.com"

class searchES(): 
    def __init__(self, index_name): 
        self.es_instance = Elasticsearch(
                                hosts=[HOST],
                                http_auth=awsauth,
                                use_ssl=True,
                                verify_certs=True,
                                connection_class=RequestsHttpConnection
                            )
        self.index = index_name
    
    def _search(self, es, index_name, query_body, offset, size):
        res = es.search(index=index_name, body=query_body, from_=offset, size=size)
        hits = [hit['_source'] for hit in res['hits']['hits']]
        return hits
    
    def search_es(self, cuisine_type, num_restaurants): 
        # get random offset
        size = num_restaurants
        offset = random.randint(0, 600)
        query = {'query': {'match': {'cuisine': cuisine_type}}}
        hits = self._search(self.es_instance, self.index, query, offset, size)
        return hits
