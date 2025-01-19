from dotenv import load_dotenv
import requests
from os import getenv
import google.generativeai as genai
from random import randint, randrange, uniform, random
import time
from datetime import datetime as dtime, timedelta
from pprint import pprint
import re
import json
import numpy as np
from poller import GeminiPoller
import pandas as pd
from sqlalchemy import create_engine
import logging
import sys
from datetime import datetime
import pytz
import idna
import smtplib

load_dotenv(dotenv_path='/home/alice/ShitCode/reviews-generator/.env')



if __name__ == "__main__":
    print('')
    # items['email_sended'] = False
    # print(items)
    # items.to_csv('otzovik_item.csv', index=False)
    # db_engine = create_engine('postgresql+psycopg2://{user}:{pswd}@{host}:{port}/{name}'.format(
    #     user=getenv('DB_USER'),
    #     pswd=getenv('DB_PSWD'),
    #     host=getenv('DB_HOST'),
    #     port=getenv('DB_PORT'),
    #     name=getenv('DB_NAME')
    # ))

    # data = pd.read_sql_query(
    #     """
    #     SELECT
    #         item.id,
    #         item.name,
    #         item.description,
    #         item.address,
    #         subs.name as subctg,
    #         ctgs.name as ctg
    #     FROM
    #         otzovik_api_item item
    #     JOIN
    #         otzovik_api_subcategory subs ON item.from_subcategory_id = subs.id
    #     JOIN
    #         otzovik_api_category ctgs ON subs.category_id = ctgs.id
    #     WHERE
    #         item.email <> '' and item.description <> ''
    #     """,
    #     con=db_engine
    # )

    # data = pd.read_sql_query(
    #     """
    #     SELECT
    #         *
    #     FROM
    #         otzovik_api_comment
    #     LIMIT
    #         1
    #     """,
    #     con=db_engine
    # )

    # reviews = pd.DataFrame(columns=[
    #     'date',
    #     'content',
    #     'user_pars',
    #     'mark',
    #     'on_item_id',
    # ])

    # review = pd.Series(
    #     [datetime(2024, 10, 1, 12, 0, 0, tzinfo=pytz.UTC), 'Тестовый отзыв', 'Антон', 5, 1],
    #     index=['date', 'content', 'user_pars', 'mark', 'on_item_id']
    # )

    # reviews = pd.concat([reviews, review.to_frame().T], ignore_index=True)

    # reviews.to_sql('otzovik_api_comment', db_engine, if_exists='append', index=False)

    # print(reviews)
    # print(data)

    # data.to_csv('data/otzovik_item.csv')



    # print(data['subctg'] + data['ctg'])
    # data = ['сколько ног у двери?', '', '', '', '', '','','','','','Ты покемон?']
    # prof = pd.read_csv('data/professions.csv')

    # prof.to_json('data/prof.json', orient='records', lines=True, index=False, force_ascii=False)

    # print(prof)
    # prof[prof.isna().any(axis=1)].to_csv('fall_professions.csv', index=False, encoding='utf-8')
    
    # prof.dropna().to_csv('professions.csv', index=False, encoding='utf-8')

    # prof.apply(
    #      lambda item: print(item['profession']) if item['female_odds'] == 'NaN' else None, axis=1
    # )
    
    # prof.sort_values(by='profession').to_csv('data/professions.csv', index=False, encoding='utf-8')
    # print(prof)

    # professions = pd.read_csv('data/fall_professions.csv')
    # professinons_with_odds = pd.DataFrame()

    # gemini_conveyor_belt = GeminiPoller()
    # try:
    #     i = 0
    #     length = len(professions)
    #     while gemini_conveyor_belt.is_run and i < length:
    #         prompt = f'Скажи, кто чаще работает в этой профессии "{professions.loc[i, 'profession']}", мужчины или женщины? Дай ответ в приблизительной процентном соотношении. В формате JSON {"{'male': процент, 'female': процент}"}.'
    #         answer = gemini_conveyor_belt.request_handler(prompt=prompt)

    #         answer = answer[answer.find('{'): answer.find('}')]

    #         male_odds = answer[:answer.find(',')]
    #         male_odds = re.sub(r"^\s+|\n|\r|\s+$", '', male_odds)
    #         male_odds = re.sub('"', '', male_odds)

    #         female_odds = answer[answer.find(','):]
    #         female_odds = re.sub(r"^\s+|\n|\r|\s+$", '', female_odds)
    #         female_odds = re.sub('"', '', female_odds)
    
    #         nrow = pd.Series((professions.loc[i, 'profession'], female_odds, male_odds),
    #             index=['profession', 'female_odds', 'male_odds'])
            
    #         professinons_with_odds = pd.concat([professinons_with_odds, nrow.to_frame().T], axis=0)

    #         i += 1
    # except KeyboardInterrupt:
    #     gemini_conveyor_belt.stoped_work('User completed the script.')
    #     professinons_with_odds.to_csv('professions_with_odds.csv', index=False, encoding='utf-8')
    # except Exception as e:
    #     gemini_conveyor_belt.stoped_work(f'Error outside the module: {e}')

    # if gemini_conveyor_belt.is_run:
    #     gemini_conveyor_belt.stoped_work('All data has been processed.')
    
    # professinons_with_odds.to_csv('professions_with_odds.csv', index=False, encoding='utf-8')


# fake = Faker('ru_RU')

# male_jobs = []
# for _ in range(10000):
#     male_jobs.append(fake.job_male())

# male_jobs.sort()
# _male_jobs = male_jobs
# male_jobs = [_male_jobs[0]]

# for job in _male_jobs:
#     if job != male_jobs[-1]:
#         male_jobs.append(job)

# with open('male_jobs.txt', 'w', encoding='utf-8') as file:
#     for job in male_jobs:
#         file.write(f'{job}\n')

# jobs = []

# with open('male_jobs.txt', 'r', encoding='utf-8') as file:
#     for job in file.readlines():
#         jobs.append(job)

# with open('female_jobs.txt', 'r', encoding='utf-8') as file:
#     for job in file.readlines():
#         jobs.append(job)

# jobs.sort()
# _jobs = jobs
# jobs = [_jobs[0]]

# for job in _jobs:
#     if job != jobs[-1]:
#         jobs.append(job)

# with open('jobs.txt', 'w', encoding='utf-8') as file:
#     for job in jobs:
#         file.write(f'{job}')
