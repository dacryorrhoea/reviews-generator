import pandas as pd
from dotenv import load_dotenv
import requests
from os import getenv, path
from google import genai
from google.genai import types
from random import randint, randrange, uniform, random
import time
from datetime import datetime as dtime, timedelta
from pprint import pprint
import re
import json
import sys
import logging
import atexit
import shutil
import asyncio
from collections import deque
import functools
from rich.console import Console
from rich.markdown import Markdown
console = Console()

load_dotenv(dotenv_path='/home/alice/ShitCode/reviews-generator/.env')

AVAILABLE_REQUESTS_PER_DAY = 1500

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('poller.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s \n%(message)s\n", "%Y-%m-%d %H:%M:%S")
)

log.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(levelname)s \n%(message)s\n", "%Y-%m-%d %H:%M:%S")
)

log.addHandler(file_handler)
log.addHandler(console_handler)


class GeminiClient:
    MAX_CALLS = 3
    MODEL_ID = 'gemini-2.0-flash-exp'

    def __init__(self, api_key):
        self.__client = genai.Client(api_key=api_key)
        self.calls = deque()


    def query(self, prompt):
        # manage calls deque rate_limiter_per_minute_requests
        while self.calls and time.time() - self.calls[0] > 60:
                self.calls.popleft()

        if len(self.calls) < self.MAX_CALLS:
            self.calls.append(time.time())
        else:
            return {
                'is_exceeding_limit': True,
                'error': None,
                'result': None
            }

        try:
            response = self.__client.models.generate_content(
                model=self.MODEL_ID,
                contents=prompt
            )
        except Exception as err:
            return {
                'is_exceeding_limit': False,
                'error': True,
                'result': None
            }
        
        return {
            'is_exceeding_limit': True,
            'error': False,
            'result': Markdown(response.text)
        }


class GeminiPoller:
    def __init__(self):
        if not path.exists("settings.json"):
            with open('settings.json', 'w') as file:
                json.dump({
                    "api_keys": []
                }, file, indent=4)

            log.debug('Settings file has been created, add the keys.')
            sys.exit(0)

        with open('settings.json', 'r') as file:
            settings = json.load(file)
            list_api_keys = settings['api_keys']

        # checking correctness keys list
        if not len(list_api_keys) or not all(key != "" for key in list_api_keys):
            log.error('List of keys empty.')
            sys.exit(1)

        self.clients = []
        for i, key in enumerate(list_api_keys):
            self.clients.append(GeminiClient(api_key=key))
            log.debug(f'Init client №{i+1}, used key - "{key[:5]}...{key[-5:]}".')

        log.debug('Poller is init.')
        
    
    def send_prompt(self, prompt):
        clients = iter(self.clients)

        tries = 0
        client = next(clients)
        while True:
            # print(client)
            answer = client.query(prompt=prompt)
            if answer['result']:
                return answer['result']

            if answer['error']:
                break

            # if answer['is_exceeding_limit']:
            #     print('limit!')

            try:
                client = next(clients)
            except StopIteration:
                clients = iter(self.clients)
                tries += 1
                continue

        return None
        
    

if __name__ == '__main__':
    poll = GeminiPoller()

    text = poll.send_prompt('сколько ног у двери?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у папы?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у сороки?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у кеги?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у ломбарда?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у собаки?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
    text = poll.send_prompt('сколько ног у амёбы?')
    log.debug('pip')
    console.print(text)
    print('\n----------------------------------------------------------------------\n')
ыва
    # try:
    #     while 1:
    #         poll.request_handler(input(' -> '))
    # except KeyboardInterrupt:
    #     poll.stoped_work('кртл ц')
