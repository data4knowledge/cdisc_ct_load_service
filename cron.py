import sys
import json
import time
import requests

local = 'http://localhost:8000/'
remote = 'https://cq8mqy.deta.dev/'
use_url = local
headers =  {"Content-Type":"application/json"}

def root():
  print(f'Sending ...')
  x = requests.get(use_url, headers=headers)
  if x.status_code == 200:
    print(f'Success, data: {x.json()}')
  else:
    print(f'Failed, code: {x.status_code}, info: {x.content}')

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
  url = "%sactions" % (use_url)
  execute = True
  while execute:
    print(f'Sending ...')
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
      data = response.json()
      print(f'Success, data: {data}')
      if not target == None and data['action_count'] == target:
        execute = False
    else:
      print(f'Failed, code: {response.status_code}, info: {response.content}')
      execute = False
    time.sleep(0.1)

def action():
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
  kwargs = dict(arg.split('=') for arg in sys.argv[1:])
  if "target" in kwargs:
    target = int(kwargs['target'])
  if "config" in kwargs:
    run_config = str2bool(kwargs['config'])
  print("MAIN [1]: Target=%s, Run Configuration=%s" % (target, run_config))
  if run_config:
    print("MAIN [2]: Configuring")
    config()
  action_until(target)