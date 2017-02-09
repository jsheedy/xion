#!/usr/bin/env python

import os

import json
from xion.xion import Xion

dirname = os.path.dirname(__file__)
comms = os.path.join(dirname, 'data.json')

data = json.load(open(comms))

xion = Xion()

for record in data:
    body = record['body']
    xion.train(body)

xion.normalize()

for i in range(5):
    print('-----------')
    print(xion.speak())