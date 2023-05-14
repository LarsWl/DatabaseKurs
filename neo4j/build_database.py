from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship

client = Elasticsearch(hosts=[{ "host": "localhost", "scheme": "http", "port": 9200}])

lessons = client.search(index="lessons", size=10000).body["hits"]["hits"]
trainers = client.search(index="trainers", size=10000).body['hits']['hits']

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminegor")

graph_db = Graph(URI, auth=AUTH)
graph_db.delete_all()

VISITOR_NODE_NAME = "Visitor"
TRAINER_NODE_NAME = "Trainer"
RELATIONSHIP_NAME = "WorkoutWith"

number_of_rels = 0;
for trainer in trainers:
    try:
        trainer_node = Node(
            TRAINER_NODE_NAME,
            id=trainer["_id"],
            speciality=trainer['_source']['speciality'],
            work_experience=trainer['_source']['work_experience'],
            personal_info=trainer['_source']['personal_info']
        )
        graph_db.create(trainer_node)
    except Exception as e:
        print(e);
        continue

    lesson_req = {
        "term": {
            "trainer_id": trainer["_id"]
        }
    }

    lessons = client.search(index="lessons", query=lesson_req).body["hits"]["hits"]

    for lesson in lessons:
        try:
            visitor_node = graph_db.nodes.match(VISITOR_NODE_NAME, id=lesson['_source']['visitor_id']).first()

            if visitor_node == None:
                visitor_node = Node(
                    VISITOR_NODE_NAME,
                    id=lesson['_source']['visitor_id'],
                    personal_info=lesson['_source']['personal_info']
                )
                graph_db.create(visitor_node)
            
            number_of_rels+=1
            req = 'MATCH (a:Visitor), (b:Trainer)\n' + \
                f'WHERE a.id = "{visitor_node["id"]}" AND b.id = "{trainer_node["id"]}"\n' + \
                f'CREATE (a)-[r:WorkoutWith {{date: "{lesson["_source"]["date"]}"}}]->(b)'

            print(req)
            graph_db.run(req)

            print(graph_db.run("MATCH ()-[r:WorkoutWith]->() with r RETURN count(r);"))
        except Exception as e:
         print(e)
         continue


print(number_of_rels)


