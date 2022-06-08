from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store

class ActionScheme(Action):
  scheme: str
  date: str

  def __init__(self, *args, **kwargs):
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__config = Configuration()
    self.__actions = self.__store.get("list")
    super().__init__(*args, **kwargs)

  def process(self):
    list = []

  def to_preserve(self):
    return { 'scheme': self.scheme, 'date': self.date }
    