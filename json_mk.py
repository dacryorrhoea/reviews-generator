import json
from faker import Faker

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

jobs = []

with open('male_jobs.txt', 'r', encoding='utf-8') as file:
    for job in file.readlines():
        jobs.append(job)

with open('female_jobs.txt', 'r', encoding='utf-8') as file:
    for job in file.readlines():
        jobs.append(job)

jobs.sort()
_jobs = jobs
jobs = [_jobs[0]]

for job in _jobs:
    if job != jobs[-1]:
        jobs.append(job)

with open('jobs.txt', 'w', encoding='utf-8') as file:
    for job in jobs:
        file.write(f'{job}')
