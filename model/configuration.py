from typing import List
from pydantic import BaseModel
from datetime import date, datetime
from model.manifest import Manifest
from store.store import Store
import json

START_DATE = 'start_date'
RELEASES = 'releases'
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

  def fix_start_date(self, requested_date):
    self.start_date = self.__manifest.next_release_after(requested_date)
    self.__store.put(START_DATE, self._to_iso8601_str(self.start_date))

  def set_release_list(self):
    self.releases = self.__manifest.release_list(self.start_date)
    print(self.releases)
    self.__store.put(RELEASES, json.dumps([self._to_iso8601_str(i) for i in self.releases]))

  def _read_start_date(self):
    data = self.__store.get(START_DATE)
    if data != None:
      self.start_date = self._from_iso8601_str(data)
    else:
      self.start_date = datetime(INITIAL_RELEASE_YEAR, 1, 1)

  def _read_releases(self):
    data = self.__store.get(RELEASES)
    if data == None:
      self.releases = []
    else:
      data = json.loads(data)
      self.releases = [self._from_iso8601_str(i) for i in data]
    
  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()
  
  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")