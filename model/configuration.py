from pydantic import BaseModel
from datetime import date, datetime
from model.manifest import Manifest
from store.store import Store

class ConfigurationPost(BaseModel):
  start_date: date
  
class Configuration():
  start_date: date

  def __init__(self):
    self.__store = Store()
    store_date = self.__store.get("start_date")
    if store_date != None:
      self.start_date = datetime.strptime(store_date, '%Y-%m-%d').date()
    else:
      self.start_date = datetime(2007, 1, 1)

  def fix_start_date(self, requested_date):
    manifest = Manifest()
    self.start_date = manifest.next_after(requested_date)
    self.__store.put("start_date", self.start_date.strftime("%Y-%m-%d"))
