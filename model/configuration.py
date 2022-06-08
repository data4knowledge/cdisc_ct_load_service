from typing import List
from pydantic import BaseModel
from datetime import date, datetime
from store.store import Store
from model.manifest import Manifest
import json

START_DATE = 'start_date'
INITIAL_RELEASE_YEAR = 2007

class ConfigurationIn(BaseModel):
  start_date: date
  
class Configuration():
  start_date: date

  def __init__(self):
    self.__store = Store("name_value")
    self.__manifest = Manifest()
    self._read_start_date()

  def set_start_date(self, requested_date):
    self.start_date = self.__manifest.next_release_after(requested_date)
    self.__store.put(START_DATE, self._to_iso8601_str(self.start_date))

  def _read_start_date(self):
    data = self.__store.get(START_DATE)
    if data != None:
      self.start_date = self._from_iso8601_str(data)
    else:
      self.start_date = datetime(INITIAL_RELEASE_YEAR, 1, 1)

  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()
  
  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")