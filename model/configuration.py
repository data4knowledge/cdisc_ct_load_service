from typing import List
from pydantic import BaseModel
from datetime import date, datetime
from model.manifest import Manifest
from store.store import Store
import json

START_DATE = 'start_date'
RELEASE = 'release'
THESAURUS = 'thesaurus'
CODE_LIST = 'code_list'
INITIAL_RELEASE_YEAR = 2007

class ConfigurationPost(BaseModel):
  start_date: date
  
class Configuration():
  start_date: date
  releases: List[date]

  def __init__(self):
    self.__store = Store()
    self.__manifest = Manifest()
    self._read_start_date()
    self._read_releases()
    self.thesauri = []
    self.code_lists = []

  def set_start_date(self, requested_date):
    self.start_date = self.__manifest.next_release_after(requested_date)
    self.__store.put(START_DATE, self._to_iso8601_str(self.start_date))

  def set_releases(self):
    self.releases = self.__manifest.release_list(self.start_date)
    self.__store.put(RELEASE, json.dumps([self._to_iso8601_str(i) for i in self.releases]))

  def set_thesauri(self):
    self.code_lists = [] # To come
    self.__store.put(THESAURUS, json.dumps(self.thesauri))

  def set_code_lists(self):
    self.code_lists = [] # To come
    self.__store.put(CODE_LIST, json.dumps(self.code_lists))

  def _read_start_date(self):
    data = self.__store.get(START_DATE)
    if data != None:
      self.start_date = self._from_iso8601_str(data)
    else:
      self.start_date = datetime(INITIAL_RELEASE_YEAR, 1, 1)

  def _read_release(self):
    data = self.__store.get(RELEASE)
    if data == None:
      self.releases = []
    else:
      data = json.loads(data)
      self.releases = [self._from_iso8601_str(i) for i in data]
    
  def _read_thesauri(self):
    data = self.__store.get(THESAURUS)
    if data == None:
      self.thesauri = []
    else:
      self.thesauri = json.loads(data)

  def _read_code_lists(self):
    data = self.__store.get(CODE_LIST)
    if data == None:
      self.code_lists = []
    else:
      self.code_lists = json.loads(data)
    
  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()
  
  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")