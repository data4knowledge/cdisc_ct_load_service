from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store

class ActionRelease(Action):
  release_date: str

  def __init__(self, *initial_data, **kwargs):
    print("ID:", initial_data)
    print("KW:", kwargs)
    self.release_date = kwargs.pop('release_date')
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__config = Configuration()
    super().__init__(*initial_data, **kwargs)
    
  def process(self):
    list = self.__manifest.concept_scheme_list(self.release_date)
