from fastapi import FastAPI
from model.configuration import *
from model.action_list import *

VERSION = "0.1"
SYSTEM_NAME = "d4k CT Load Microservice"

app = FastAPI()

@app.get("/")
def read_root():
  return { 'version': VERSION, 'system': SYSTEM_NAME }

@app.post("/configuration")
def create_configuration(config: ConfigurationPost):
  saved_config = Configuration()
  saved_config.set_start_date(config.start_date)
  actions = ActionList(saved_config)
  actions.add_releases()
  return { 'status': 'ok' }

#@app.lib.cron()
#def cron_job(event):
#  return { 'status': 'cron' }
# @app.post("/action")
# def create_action():
#   config = Configuration()
#   actions = Action()
#   actions.next(config)
#   return { 'status': 'ok' }
