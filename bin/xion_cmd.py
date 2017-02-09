#!/usr/bin/env python

import json
from xion import Xion

comms = 'data.json'

data = json.load(open(comms))

xion = Xion()

for record in data:
    body = record['body']
    xion.train(body)

xion.normalize()

for i in range(5):
    print('-----------')
    print(xion.speak())