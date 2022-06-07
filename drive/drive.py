from deta import Deta
import os
#import yaml

class Drive():
    
  def __init__(self):
    self.__deta = Deta(os.environ['CDISC_CT_LOAD_SERVICE_PROJ_KEY'])
    
  def read(self, name, filename):
    drive = self.__deta.Drive("cdisc_ct.%s" % (name))
    data = yaml.safe_load(drive.get(filename))
    return data
