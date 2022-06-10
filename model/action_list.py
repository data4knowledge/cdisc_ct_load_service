import json
from model.configuration import Configuration
from model.manifest import Manifest
from model.action_release import ActionRelease
from model.action_scheme import ActionScheme
from store.store import Store

STORE_KEY = "list"

class ActionList():
  
  def __init__(self):
    self.__store = Store()
    self.__manifest = Manifest()
    self.__config = Configuration()
    self.__actions = self.__store.get(STORE_KEY)

  def add_releases(self):
    dates = self.__manifest.release_list(self.__config.start_date)
    self.__store.put([ActionRelease(release_date=i).preserve() for i in dates], STORE_KEY)

  def next(self):
    data = self.__actions[0]
    klass = globals()[data['klass']]
    action = klass(**data['data'])
    del self.__actions[0]
    new_actions = action.process()
    self.__store.put(new_actions + self.__actions, STORE_KEY)
    self.__actions = self.__store.get(STORE_KEY)

  def list(self):
    return self.__actions
  