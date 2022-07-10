import sys
import json
import time
import requests
from datetime import datetime

local = 'http://localhost:8000/'
remote = 'https://cq8mqy.deta.dev/'
use_url = local
headers =  {"Content-Type":"application/json"}

def first():
  x = requests.get("%sactions" % (use_url), headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')

def root():
  print(f'Sending ...')
  x = requests.get(use_url, headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')
    first()

def config(start_date):
  the_data = { "start_date": start_date }
  print(f'Sending ...')
  url = "%sconfigurations" % (use_url)
  x = requests.post(url, data=json.dumps(the_data), headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')

def action_until(until):
  errors = 0
  highest_errors = 0
  url = "%sactions" % (use_url)
  execute = True
  until_dt = datetime.strptime(until, '%Y-%m-%d')
  while execute:
    print("Sending [%s, %s]... " % (errors, highest_errors))
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
      errors = 0
      data = response.json()
      print(f'Success, data: {data}')
      if "release_date" in data['next']:
        current_dt = datetime.strptime(data['next']['release_date'], '%Y-%m-%d')
      elif "date" in data['next']:
        current_dt = datetime.strptime(data['next']['date'], '%Y-%m-%d')
      else:
        current_dt = datetime.strptime("2000-01-01", '%Y-%m-%d')
      print(f'Check {current_dt} versus until {until_dt}')
      if current_dt >= until_dt:
        execute = False
      else:
        time.sleep(0.1)
    else:
      print(f'Failed, code: {response.status_code}, info: {response.content}')
      first()
      if errors > 3:
        execute = False
      else:
        errors += 1
        if errors > highest_errors:
          highest_errors = errors
        time.sleep(1.0) # Long delay

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
  run_config = False
  start_date = "2000-01-01"
  until_date = "2023-01-01"
  kwargs = dict(arg.split('=') for arg in sys.argv[1:])
  if "config" in kwargs:
    run_config = str2bool(kwargs['config'])
  if "until" in kwargs:
    until_date = (kwargs['until'])
  if "start" in kwargs:
    start_date = (kwargs['start'])
  print("MAIN [1]: Start=%s, Until=%s, Run Configuration=%s" % (start_date, until_date, run_config))
  if run_config:
    print("MAIN [2]: Configuring")
    config(start_date)
  else:
    print("MAIN [3]: Running")
    action_until(until_date)