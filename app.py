import os
import sys
import json
import random
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, request

app = Flask(__name__)

# Webhook
@app.route('/', methods=['POST'])
def webhook():
  data = request.get_json()
  log('Recieved {}'.format(data))
  msg = ''
  if (data['name'] == 'Micah The Major Prophet') or (data['sender_id'] == 'PUT_SENDER_ID_HERE'): # the bot only mirrors one user
    text = data['text']
    time.sleep(1)
    send_message(mock(text))
  return "ok", 200

def mock(text, diversity_bias=0.5, random_seed=None):
  # Error handling
  if diversity_bias < 0 or diversity_bias > 1:
    raise ValueError('diversity_bias must be between the inclusive range [0,1]')
  # Seed the random number generator
  random.seed(random_seed)
  # Mock the text
  out = ''
  last_was_upper = True
  swap_chance = 0.5
  for c in text:
    if c.isalpha():
      if random.random() < swap_chance:
        last_was_upper = not last_was_upper
        swap_chance = 0.5
      c = c.upper() if last_was_upper else c.lower()
      swap_chance += (1-swap_chance)*diversity_bias
    out += c
  return out

# DO NOT MODIFY ANYTHING BELOW THIS LINE
def send_message(msg):
  url  = 'https://api.groupme.com/v3/bots/post'
  data = {
          'bot_id' : os.getenv('GROUPME_BOT_ID'),
          'text'   : msg,
         }
  request = Request(url, urlencode(data).encode())
  json = urlopen(request).read().decode()

def log(msg):
  print(str(msg))
  sys.stdout.flush()
