from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store

class ActionRelease(Action):
  release_date: str

  def __init__(self, *args, **kwargs):
    print("ID:", args)
    print("KW:", kwargs)
    self.release_date = kwargs.pop('release_date')
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__config = Configuration()
    super().__init__(*args, **kwargs)
    
  def process(self):
    return self.__manifest.concept_scheme_list(self.release_date)

  def to_preserve(self):
    return { 'release_date': self.release_date }