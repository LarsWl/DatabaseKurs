import random
import uuid
import json

TRAINERS_INDEX = 'trainers'
LESSONS_INDEX = 'lessons'
TRAINER_DOC_TYPE = 'trainer'
LESSON_DOC_TYPE = 'lesson'

possible_specialities = [
    'Фитнес', 'Легкая атлетика', 'Карате', 'Бокс',
    'Борьба', 'Фехтование', 'Плавание', 'Футбол'
]

possible_reviews = [
    'Все понравилось', 'Ужасно, результата никакого',
    'Хорошо консультирует', 'Не очень понравились упраженения, но в целом хорошо',
    'Приятный человек, поддерживает', 'Никак не помогает', 'Есть как плюсы, так и минусы',
    'Составил диету, очень довольна', 'Не смог помочь сбросить вес', 'Очень довольна',
    'Может опаздывать на занятия, но проводит их  хорошо', 

]

possible_work_experience = list(range(1, 20))

male_names = ['Михаил', 'Сергей', 'Дмитрий', 'Богдан', 'Алексей', 'Антон', 'Евгений', 'Роман', 'Максим']
female_names = ['Дарья', 'Александра', 'Ксения', 'Татьяна', 'Евгения', 'Юлия', 'Мария', 'Анна']

possible_ages = list(range(25, 55))
possible_prices = list(range(500, 2500, 200))
possible_services = [
    'Составление плана тренировок', 'Проведение тренировки', 'Составление диеты',
    'Баня', 'Бассейн', 'Групповое занятие', 'Предоставление экипировке'
]

def build_personal_info():
    sex = random.choice(['М', 'Ж'])
    age = random.choice(possible_ages)

    if sex == 'М':
        name = random.choice(male_names)
    else:
        name = random.choice(female_names)

    return 'Имя: {}, возраст: {}, пол: {}'.format(name, age, sex)

def build_trainer():
    reviews_number = random.randint(1, 3)

    return {
        'index': TRAINERS_INDEX,
        'doc_type': TRAINER_DOC_TYPE,
        'id': str(uuid.uuid4()),
        'body': {
            'speciality': random.choice(possible_specialities),
            'work_experience': random.choice(possible_work_experience),
            'personal_info': build_personal_info(),
            'reviews': random.sample(possible_reviews, k=reviews_number)
        }
    }

def build_date():
    day = str(random.randint(1,25))
    if len(day) == 1:
        day = '0' + day

    month = str(random.randint(1,12))
    if len(month) == 1:
        month = '0' + month

    return "{}-{}-{}".format(day, month, random.randint(2022, 2023))


def build_abonement():
    number_of_lessons = random.randint(5,50)

    return 'Абонемент на {} занятий. Специальность: {}'.format(number_of_lessons, random.choice(possible_specialities))

def build_lesson(trainers, visitors):
    lesson_id = str(uuid.uuid4())
    number_of_services = random.randint(1, 5)
    visitor = random.choice(visitors)

    return {
        'index': LESSONS_INDEX,
        'doc_type': LESSON_DOC_TYPE,
        'id': lesson_id,
        'body': {
            'trainer_id': random.choice(visitor['possible_trainers'])['id'],
            'lesson_id': lesson_id,
            'visitor_id': visitor['id'],
            'date': build_date(),
            'age': visitor['age'],
            'abonement': visitor['abonement'],
            'services': random.sample(possible_services, k=number_of_services),
            'price': random.choice(possible_prices),
            'personal_info': visitor['personal_info'],
        }
    }

def build_visitor(trainers):
    return {
        "personal_info": build_personal_info(),
        "age": random.choice(possible_ages),
        "id": str(uuid.uuid4()),
        "abonement": build_abonement(),
        "possible_trainers": random.sample(trainers, k=3)
    }


def generate_docs():
    number_of_trainers = 20
    number_of_lessons = 40
    number_of_visitors = 5

    trainers = [build_trainer() for i in range(0, number_of_trainers)]
    visitors = [build_visitor(trainers) for i in range(0, number_of_visitors)]
    lessons = [build_lesson(trainers, visitors) for i in range(0, number_of_lessons)]

    with open('trainers.json', 'w', encoding='utf-8') as f:
        json.dump(trainers, f, ensure_ascii=False)

    with open('lessons.json', 'w', encoding='utf-8') as f:
        json.dump(lessons, f, ensure_ascii=False)


generate_docs()

