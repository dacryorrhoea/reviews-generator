import pandas as pd
from dotenv import load_dotenv
import requests
from os import getenv, path
import google.generativeai as genai
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


class GeminiPoller:
    def __init__(self):
        # create a settings file if it not exist
        if not path.exists("settings.json"):
            with open('settings.json', 'w') as file:
                json.dump({
                    "requests_count": 0,
                    "last_request": str(dtime.now()),
                    "api_keys": []
                }, file, indent=4)

            log.debug('Settings file has been created, add the keys.')
            sys.exit(0)

        # checking the correctness of the file
        with open('settings.json', 'r') as file:
            try:
                settings = json.load(file)
            except json.JSONDecodeError:
                log.error('You ruined json file.')
                sys.exit(1)

        # to set requests count, last request time, api_keys - if they exist
        try:            
            self.requests_count = settings['requests_count']
            self.last_request = dtime.fromisoformat(settings['last_request'])
            list_api_keys = settings['api_keys']
        except Exception:
            log.error('You all ruined. Recreate settings file.')
            sys.exit(1)

        # checking keys list exist
        if not len(list_api_keys) or not all(key != "" for key in list_api_keys):
            log.error('List of keys empty.')
            sys.exit(1)

        self.api_keys = iter(list_api_keys)
        self.number_available_requests = len(list_api_keys) * AVAILABLE_REQUESTS_PER_DAY

        api_key = next(self.api_keys)
        self.ai_client = genai.Client(api_key=api_key)

        log.debug(f'Ai instance is init, current api key - "{api_key[:5]}...{api_key[-5:]}".')

        atexit.register(self.stoped_work)

        log.debug('Poller is init.')
        
    
    def change_api_key(self):
        try:
            api_key = next(self.api_keys)
        except StopIteration:
            log.debug('Run out of keys.')
            return 1

        genai.configure(api_key=api_key)
        self.ai_client = genai.GenerativeModel('gemini-2.0-flash-exp')

        log.debug(f'Api key is change, current - "{api_key[:5]}...{api_key[-5:]}".')
        return 0

    
    def timeout(self):
        pass_time = dtime.now() - self.last_request

        if pass_time.total_seconds() < 6:
            time.sleep(6 - pass_time.total_seconds())

        self.last_request = dtime.now()


    def request_handler(self, prompt):
        answer = None
        self.timeout()
        response = self.ai_client.generate_content(prompt)
        answer = response.text

        # just for pretty log
        column = shutil.get_terminal_size().columns
        log.debug(
            f' -> Response time: {(dtime.now() - self.last_request).total_seconds():.2f} sec\n'
            f' -> Prompt: {prompt.replace('\n', ' ')[:(column*2)-12]}\n'
            f' -> Answer: {answer.replace('\n', ' ')}\n'
        )
        
        return answer
    

    def stoped_work(self, reason):
        with open('settings.json', 'r+') as file:
            settings = json.load(file)
            file.seek(0)
            json.dump({
                'requests_count': self.requests_count,
                'last_request': str(self.last_request),
                'api_keys': settings['api_keys']
            }, file, indent=4)


if __name__ == '__main__':
    poll = GeminiPoller()
    try:
        while 1:
            poll.request_handler(input(' -> '))
    except KeyboardInterrupt:
        poll.stoped_work('кртл ц')

    poll.stoped_work('конец')