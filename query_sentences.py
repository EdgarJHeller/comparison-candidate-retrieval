import requests
import sys
from requests.auth import HTTPBasicAuth
import json


ES_HOSTNAME = 'http://ltdemos.informatik.uni-hamburg.de/depcc-index/'
INDEX = 'depcc'
CRAWL_DATA_REPOS = '/_search?q='


def build_url(comparison_object, vs):
    base_url = ES_HOSTNAME + INDEX + CRAWL_DATA_REPOS
    return base_url + 'text:(\"{}\"%20AND%20\"{}\")&from=0&size=10000'.format(comparison_object, vs)


def retrieve_sentences(comparison_object, vs='vs'):
    url = build_url(comparison_object, vs)
    print(url)
    if(len(sys.argv) > 1):
        es_json = requests.get(url, auth=HTTPBasicAuth(sys.argv[1], sys.argv[2]))
    else:
        es_json = requests.get(url)

    return extract_sentences(es_json)


def extract_sentences(es_json):
    hits = es_json.json()['hits']['hits']
    sentences = []
    for hit in hits:
        text = hit['_source']['text']
        sentences.append(text)

    return sentences
