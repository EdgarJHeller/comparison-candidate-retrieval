from elasticsearch import Elasticsearch
import re

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'dt-index'

es = Elasticsearch(hosts = [ES_HOST], timeout=300)

def filter(comparison_object, candidates):
    similarities_comparison_object = get_all_similarities(comparison_object)
    filtered_candidates = []
    for candidate in candidates:
        print('---', candidate, '---')

        if any(candidate[0] == s or candidate[0] == re.sub('[^a-zA-Z0-9 ]', '', s)  for s in similarities_comparison_object):
            filtered_candidates.append(candidate[0])    
        
        # print([s for s in similarities_comparison_object if candidate[0] == s])


    return filtered_candidates[0:10]



def get_all_similarities(comparison_object):
    print(comparison_object)
    res = es.search(index = INDEX_NAME, size=10000, body={"query": {"match": {"first": comparison_object}}})

    # similar_words = [re.sub('[^a-zA-Z0-9 ]', '', hit['_source']['second']) for hit in res['hits']['hits']]

    return [hit['_source']['second'] for hit in res['hits']['hits']]