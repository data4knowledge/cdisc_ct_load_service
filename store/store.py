from deta import Deta
import json
import os

class Store():
    
  def __init__(self, sub_base):
    self.__deta = Deta(os.environ['CDISC_CT_LOAD_SERVICE_PROJ_KEY'])
    self.__store = self.__deta.Base('cdisc_ct_load_service.%s' % (sub_base))
    
  def put(self, key, data):
    self.__store.put(data, key)

  def get(self, key):
    data = self.__store.get(key)
    if data == None:
      return None
    else:
      return data['value']

