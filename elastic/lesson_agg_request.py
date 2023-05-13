from elasticsearch import Elasticsearch
import json


client = Elasticsearch(hosts=[{ "scheme": "http", "host": "localhost", "port": 9200}])

with open('lessons_agg.json', 'r') as f:
    request = json.load(f)

index = "lessons"

res = client.search(index=index, aggs=request['aggs'], size=1)

print(json.dumps(res.body, indent=4,ensure_ascii=False))
