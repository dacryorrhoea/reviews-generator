from datetime import datetime
import requests
import time
import google.generativeai as genai
import random
import os
from os import getenv
from dotenv import load_dotenv
from pprint import pprint
import json
from random import choice, randint, randbytes
from faker import Faker
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine

from poller import GeminiPoller

load_dotenv(dotenv_path='/home/alice/ShitCode/reviews-generator/.env')


class ReviewsGenerator:
    def __init__(self):
        self.ai_poller = GeminiPoller()

        with open("data/synthetic_data.json", "r") as file:
            self.names = json.load(file)

        self.professions = pd.read_csv('data/professions.csv')


    def char_generate(self):
        age = str(randint(18, 70))
        if age[1] in ('2', '3', '4'):
            age += ' года'
        elif age[1] == '1':
            age += ' год'
        else:
            age += ' лет'

        prof = self.professions.sample(n=1).squeeze()

        profession = prof['profession']

        f = randint(1, 100)
        sex = 'женщина' if f <= float(prof['female_odds']) else 'мужчина'
        
        first_name = choice(self.names['female' if sex == 'женщина' else 'male']['first_name'])
        last_name = choice(self.names['female' if sex == 'женщина' else 'male']['last_name'])
        patronymics = choice(self.names['female' if sex == 'женщина' else 'male']['patronymics'])

        prompt = f"""Пожалуйста, придумай один вариант, "О себе", без необходимости его дополнять, для {sex[:-1]}ы возрастом {age}, {
                    'которую' if sex == 'женщина' else 'которого'
                } зовут {first_name} c фамилией {last_name} и отчеством {patronymics}. Профессия {'которой' if sex == 'женщина' else 'которого'} - {profession}. Так же укажи, что этому человеку нравится, а что противно. В каком семейном положеннии состоит. В каком городе Беларуси проживает. 
            """
        
        desc = self.ai_poller.request_handler(prompt=prompt)

        return {
            'first_name': first_name,
            'last_name': last_name,
            'patronymics': patronymics,
            'sex': sex,
            'age': age,
            'profession': profession,
            'bio': desc
        }


    def review_generate(self, subject, rating):
        person = self.char_generate()

        rate = 'позитивный'
        if rating < 3:
            rate = 'негативный'
        elif rating == 3:
            rate = 'нейтральный'

        if rating > 3:
            emotion = 'осталась довольна' if person['sex'] == 'женщина' else 'остался доволен'
        else:
            emotion = 'осталась недовольна' if person['sex'] == 'женщина' else 'остался недоволен'
        
        verb = 'взаимодействовала' if person['sex'] == 'женщина' else 'взаимодействовал'
    
        roleplay_review = self.ai_poller.request_handler(
            'Привет! Я {person_name}, мне {person_age}, расскажу немного о себе: \n{person_bio}.\n'
            'И в общем, недавно я {person_verb} с организацией {subj_name} и {person_emotion}. '
            'Моя оценка организации - {rating}/5. Поэтому напиши пожалуйста {rate} отзыв '
            'от моего лица. Но не используй моё имя. А что именно случилось придумай сам. '
            'Отзыв небольшой, максимум на 800 символов. Слова используй попроще. '
            'Без Акцента на имени компании. Её адрес указывать необязательно. И самое главное - '
            'максимально правдоподобно.'
            '\nА вот информация о том что за организация и чем занимается:\n'
            '\tОбласть деятельности - {subj_ctg}, {subj_subctg}.\n'
            '\tОписание - {subj_desc}.\n'
            '\tАдресс - {subj_address}.'
            '\tСтрана - Беларусь.'
            .format(
                person_name=person['first_name'],
                person_age=person['age'],
                person_bio=person['bio'],
                person_verb=verb,
                person_emotion=emotion,
                subj_name=subject['name'],
                rating=rating,
                rate=rate,
                subj_ctg=subject['ctg'],
                subj_subctg=subject['subctg'],
                subj_desc=subject['description'],
                subj_address=subject['address']
            )
        )

        review = self.ai_poller.request_handler(
            f'Сгенерируй {rate} отзыв на {subject['name']} от лица {person}.\n'
            f'Вот описание для {subject['name']}: {subject['description']}\n'
            'Размер отзыва пусть не превышает 1500 символов.'
            'Указывать ФИО человека не надо.'
        )

        common_review = self.ai_poller.request_handler(
            f'Сгенерируй {rate} отзыв на {subject['name']} от лица {person}.\n'
            f'Вот описание для {subject['name']}: {subject['description']}\n'
            f'Отросоль: {subject['ctg']} - {subject['subctg']}.\n'
            'Размер отзыва пусть не превышает 440 символов. И используй речь попроще.'
            'Указывать ФИО человека не надо. Имя организации тоже не нужно. Больше экспрессии.'
            'Больше сленга. Знаки препинания тоже неважны.'
        )

        return {
            'object': subject['name'],
            'author': f'{person['first_name']}',
            'base_review': review,
            'common_review': common_review,
            'roleplay_review': roleplay_review,
        }

    
if __name__ == "__main__":
    data = pd.read_csv('data/otzovik_item.csv')

    reviews_generator = ReviewsGenerator()
    reviews = []
    
    try:
        _data = data.sample(n=2)
        for index, item in _data.iterrows():
            for _ in range(randint(3, 5)):
                review = reviews_generator.review_generate(
                    subject=item,
                    rating=2
                )
                if review:
                    reviews.append(review)
                else:
                    break
    except KeyboardInterrupt:
        reviews_generator.shutdown_module()
        with open('data/reviews.json', 'w', encoding='utf-8') as file:
            json.dump(reviews, file, indent=4, ensure_ascii=False)

    reviews_generator.shutdown_module()    
    with open('data/reviews.json', 'w', encoding='utf-8') as file:
        json.dump(reviews, file, indent=4, ensure_ascii=False)
