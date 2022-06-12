from deta import Deta
import os
import yaml

class Drive():
    
  def __init__(self, scheme):
    self.__deta = Deta(os.environ['CDISC_CT_LOAD_SERVICE_PROJ_KEY'])
    #print("DRIVE.__INIT__ [1]:", scheme)
    self.__drive = self.__deta.Drive("cdisc_ct.%s" % (scheme))
    
  def read(self, filename):
    #print("DRIVE.READ [1]:", self.__drive.list())
    #print("DRIVE.READ [2]:", filename)
    content = self.__drive.get(filename)
    #print("DRIVE.READ [3]:", content)
    data = yaml.safe_load(content)
    return data

  def upload(self, filename, data):
    #print("DRIVE.UPOAD [1]: %s, %s" % (filename, data))
    self.__drive.put(filename, data)
