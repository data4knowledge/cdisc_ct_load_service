from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store

class ActionScheme(Action):
  scheme: str
  date: str

  def __init__(self):
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__config = Configuration()
    self.__actions = self.__store.get("list")
    
  def process(self):
    list = []
    