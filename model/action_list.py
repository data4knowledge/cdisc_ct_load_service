import json
from model.configuration import Configuration
from model.manifest import Manifest
from model.action_release import ActionRelease
from model.action_scheme import ActionScheme
from store.store import Store

class ActionList():
  
  def __init__(self):
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__config = Configuration()
    self.__actions = self.__store.get("list")

  def add_releases(self):
    dates = self.__manifest.release_list(self.__config.start_date)
    self.__store.put([ActionRelease(release_date=self._to_iso8601_str(i)).preserve() for i in dates], "list")

  def next(self):
    data = self.__actions[0]
    print("PROCESS:", data)
    klass = globals()[data['klass']]
    print("KLASS:", klass)
    x = json.loads(data['data'])
    action = klass(**x)
    print("ACTION:", action)
    del self.__actions[0]
    list = action.process()
    print("LIST:", list)
    new_actions = [ActionScheme(scheme=k, date=v).preserve() for k, v in list.items()]
    print("REMAINING:", self.__actions)
    print("NEW:", new_actions)
    self.__store.put(new_actions + self.__actions, "list")

  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")