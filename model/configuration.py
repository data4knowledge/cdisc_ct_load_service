from typing import List
from pydantic import BaseModel
from datetime import date, datetime
from store.store import Store
from model.manifest import Manifest
import json

START_DATE = 'start_date'
INITIAL_RELEASE_DATE = "2007-01-01"

class ConfigurationIn(BaseModel):
  start_date: date
  
class Configuration():
  start_date: date

  def __init__(self):
    self.__store = Store()
    self.__manifest = Manifest()
    self._read_start_date()

  def set_start_date(self, requested_date):
    self.start_date = self.__manifest.next_release_after(requested_date)
    self.__store.put(self.start_date, START_DATE)

  def _read_start_date(self):
    data = self.__store.get(START_DATE)
    if data != None:
      self.start_date = data
    else:
      self.start_date = INITIAL_RELEASE_DATE
