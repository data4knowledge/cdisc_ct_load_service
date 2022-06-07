from model.manifest import Manifest
from model.action_release import ActionRelease
from store.store import Store

class ActionList():
  
  def __init__(self, config):
    self.__store = Store("actions")
    self.__manifest = Manifest()
    self.__actions = []
    self.__config = config

  def add_releases(self):
    dates = self.__manifest.release_list(self.__config.start_date)
    self.__store.put("actions", [ActionRelease(i).to_store() for i in dates])

  # def set_thesauri(self):
  #   self.code_lists = [] # To come
  #   self.__store.put(THESAURUS, json.dumps(self.thesauri))

  # def set_code_lists(self):
  #   self.code_lists = [] # To come
  #   self.__store.put(CODE_LIST, json.dumps(self.code_lists))

  # def _read_actions(self):
  #   data = self.__store.get("actions")
  #   if data == None:
  #     self.__actions = []
  #   else:
  #     data = json.loads(data)
  #     self.actions = [self._from_iso8601_str(i) for i in data]
    
  # def _read_thesauri(self):
  #   data = self.__store.get(THESAURUS)
  #   if data == None:
  #     self.thesauri = []
  #   else:
  #     self.thesauri = json.loads(data)

  # def _read_code_lists(self):
  #   data = self.__store.get(CODE_LIST)
  #   if data == None:
  #     self.code_lists = []
  #   else:
  #     self.code_lists = json.loads(data)
    
  # def _from_iso8601_str(self, text):
  #   return datetime.strptime(text, '%Y-%m-%d').date()
  
  # def _to_iso8601_str(self, date):
  #   return date.strftime("%Y-%m-%d")