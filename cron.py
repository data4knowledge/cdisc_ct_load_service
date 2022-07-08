import sys
import json
import time
import requests

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

def config():
  the_data = { "start_date": "2005-01-01" }
  print(f'Sending ...')
  url = "%sconfigurations" % (use_url)
  x = requests.post(url, data=json.dumps(the_data), headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')

def action_until(target=None):
  errors = 0
  highest_errors = 0
  url = "%sactions" % (use_url)
  execute = True
  while execute:
    print("Sending [%s, %s]... " % (errors, highest_errors))
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
      errors = 0
      data = response.json()
      print(f'Success, data: {data}')
      if not target == None and data['action_count'] == target:
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

def actions():
  print(f'Sending ...')
  url = "%sactions" % (use_url)
  x = requests.get(url, headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")

if __name__ == '__main__':
  target = None
  run_config = False
  run_actions = False
  kwargs = dict(arg.split('=') for arg in sys.argv[1:])
  if "target" in kwargs:
    target = int(kwargs['target'])
  if "config" in kwargs:
    run_config = str2bool(kwargs['config'])
  if "actions" in kwargs:
    run_actions = str2bool(kwargs['actions'])
    run_config = False
  print("MAIN [1]: Target=%s, Run Configuration=%s, Actions=%s" % (target, run_config, run_actions))
  if run_config:
    print("MAIN [2]: Configuring")
    config()
  if run_actions:
    actions()
  else:
    action_until(target)