import json
import re
import io
import os
import requests

with io.open('./sampleJSON/subjects.json', 'r') as srcOne, io.open('./sampleJSON/employees.json', 'r') as srcTwo:
    loadSrc = json.load(srcOne)
    loadPersons = json.load(srcTwo)

    for x in loadSrc:
        for y in loadPersons['persons']:
            if y['subjects']:
                for sub in y['subjects']:
                    if x['course_code'] == sub['course_code']:
                        x['title'] = sub['title']

    with io.open('./sampleJSON/predmeti.json', 'w+') as dst:
        json.dump(loadSrc, dst)