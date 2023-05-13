from py2neo import Graph, Node, Relationship

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "adminegor")

graph_db = Graph(URI, auth=AUTH)

try:
    cur = graph_db.run("MATCH (vis:Visitor)-[r:WorkoutWith]->(trn:Trainer) with vis, trn RETURN vis.id, trn.id, count(trn) as cnt ORDER BY cnt DESC LIMIT 10;")
except Exception as e:
    print(e)

while (cur.forward()):
    print(cur.current)
