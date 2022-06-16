from deta import Deta
import os
import yaml

class Drive():
    
  def __init__(self, scheme):
    self.__deta = Deta(os.environ['CDISC_CT_LOAD_SERVICE_PROJ_KEY'])
    self.__drive = self.__deta.Drive("cdisc_ct.%s" % (scheme))
    
  def read(self, filename):
    content = self.__drive.get(filename)
    data = yaml.safe_load(content)
    return data

  def upload(self, filename, data):
    self.__drive.put(filename, data)

  def present(self, filename):
    list_result = self.__drive.list()
    files = list_result.get("names")
    print("DRIVE.PRESENT:", files)
    if filename in files:
      return True
    return False
