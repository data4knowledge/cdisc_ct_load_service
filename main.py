from fastapi import FastAPI
from model.configuration import *
from model.action_list import *
from model.system import *

VERSION = "0.1"
SYSTEM_NAME = "d4k CT Load Microservice"

app = FastAPI()

@app.get("/")
def read_root():
  return SystemOut(**{ 'version': VERSION, 'system_name': SYSTEM_NAME })

@app.post("/configuration")
def create_configuration(config: ConfigurationIn):
  saved_config = Configuration()
  saved_config.set_start_date(config.start_date)
  actions = ActionList()
  actions.add_releases()
  return { 'status': 'ok' }

#@app.lib.cron()
#def cron_job(event):
#  return { 'status': 'cron' }

@app.post("/action")
def create_action():
  actions = ActionList()
  count = actions.next()
  return { 'status': 'ok', 'action_count': count }
