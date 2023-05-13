from elasticsearch import Elasticsearch
import json

client = Elasticsearch(hosts=[{ "scheme": "http", "host": "localhost", "port": 9200}])

with open('trainers_mapping.json', 'r') as f:
    trainers_mapping = json.load(f)

with open('lessons_mapping.json', 'r') as f:
    lessons_mapping = json.load(f)

with open('trainers.json', 'r') as f:
    trainers_docs = json.load(f)

with open('lessons.json', 'r') as f:
    lessons_docs = json.load(f)


def index_doc(client, index, doc):
    client.index(index=index, id=doc['id'], document=doc['body'])

trainers_index = 'trainers'
client.options(ignore_status=[400, 404]).indices.delete(index=trainers_index)
client.indices.create(index=trainers_index, mappings=trainers_mapping['mappings'], settings=trainers_mapping['settings'])
for doc in trainers_docs:
    index_doc(client, trainers_index, doc)

lessons_index = 'lessons'
client.options(ignore_status=[400, 404]).indices.delete(index=lessons_index)
client.indices.create(index=lessons_index, mappings=lessons_mapping['mappings'], settings=lessons_mapping['settings'])
for doc in lessons_docs:
    index_doc(client, lessons_index, doc) 

trainers_req = {
    "query": {
        'match_all': {}
    }
}

res = client.search(index=trainers_index)

print(res.body)

lessons_req = {
    "query": {
        'match_all': {}
    }
}

res = client.search(index=lessons_index)

print(res.body)
