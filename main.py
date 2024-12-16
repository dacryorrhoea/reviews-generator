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

load_dotenv(dotenv_path='/home/alice/ShitCode/gemini_generating_reviews/.env')


class CharacterGenerator:
    def __init__(self):
        with open("names.json", "r") as f: self.names = json.load(f)
        self.fake = Faker("ru_RU")

    def generation(self) -> dict | None:
        age = str(randint(18, 70 ))
        if age[1] in ('2', '3', '4'):
            age += ' года'
        elif age[1] == '1':
            age += ' год'
        else:
            age += ' лет'

        sex = 'женщина' if bool(random.getrandbits(1)) else 'мужчина'
        first_name = choice(self.names['female' if sex == 'женщина' else 'male']['first_name'])
        last_name = choice(self.names['female' if sex == 'женщина' else 'male']['last_name'])
        patronymics = choice(self.names['female' if sex == 'женщина' else 'male']['patronymics'])
        job = self.fake.job_female() if sex == 'женщина' else self.fake.job_male()
        job = job[0].lower() + job[1:]

        print('first_name' + ' - ' + first_name)
        print('last_name' + ' - ' + last_name)
        print('patronymics' + ' - ' + patronymics)
        print('sex' + ' - ' + f'{sex[:3]}.')
        print('age' + ' - ' + age)
        print('job' + ' - ' + job)

        prompt = f"""Пожалуйста, придумай один вариант, полного описания, без необходимости его дополнять, для {sex[:-1]}ы возрастом {age}, {
                    'которую' if sex == 'женщина' else 'которого'
                } зовут {first_name} c фамилией {last_name} и отчеством {patronymics}. Работа {'которой' if sex == 'женщина' else 'которого'} - {job}. Так же укажи, что этому человеку нравится, а что противно. В каком семейном положеннии состоит. В каком городе Беларуси проживает. 
            """
        
        # print(f'Promt: {prompt}\n')
        return None

        # genai.configure(api_key=getenv('API_KEY'))
        # model = genai.GenerativeModel("gemini-1.5-flash")
        # try:
        #     response = model.generate_content(prompt)
        #     print(f'Response: {response.text}')
        #     return {
        #         'first_name': first_name,
        #         'last_name': last_name,
        #         'patronymics': patronymics,
        #         'sex': f'{sex[:3]}.',
        #         'age': age,
        #         'job': job,
        #         'description': response.text
        #     }
        # except requests.exceptions.RequestException as e:
        #     print(f"Conection error: {e}")
        #     return None
        


if __name__ == "__main__":
    character_generator = CharacterGenerator()

    person = character_generator.generation()
    pprint(person)
    