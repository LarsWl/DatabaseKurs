from elasticsearch import Elasticsearch
import csv

client = Elasticsearch(hosts=[{ "host": "localhost", "scheme": "http", "port": 9200}])

lessons = client.search(index="lessons", size=10000).body["hits"]["hits"]
trainers = client.search(index="trainers", size=10000).body['hits']['hits']

with open("trainers.csv", "w", newline='') as trainers_file:
    t_writer = csv.writer(trainers_file)
    field = ["id", "work_experience", "speciality"]
    t_writer.writerow(field)

    for trainer in trainers:
        row = [
            trainer['_id'],
            trainer['_source']['work_experience'],
            trainer['_source']['speciality']
        ]
        t_writer.writerow(row)

with open('lessons.csv', 'w', newline='') as lessons_file:
    l_writer = csv.writer(lessons_file)
    field = ['id', 'date', 'visitor_id', 'trainer_id', 'price']
    l_writer.writerow(field)

    for lesson in lessons:
        row = [
            lesson['_source']['lesson_id'],
            lesson['_source']['date'],
            lesson['_source']['visitor_id'],
            lesson['_source']['trainer_id'],
            lesson['_source']['price']
        ]
        l_writer.writerow(row)


seen_visitors = set()

with open('visitors.csv', 'w', newline='') as visitors_file:
    v_writer = csv.writer(visitors_file)
    field = ['id', 'personal_info']
    v_writer.writerow(field)

    for lesson in lessons:
        visitor_id = lesson['_source']['visitor_id']

        if visitor_id not in seen_visitors:
            row = [
                visitor_id,
                lesson['_source']['personal_info']
            ]
            v_writer.writerow(row)
            seen_visitors.add(visitor_id)
