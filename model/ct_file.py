from datetime import datetime
from drive.drive import Drive

class CtFile():

  def __init__(self, scheme, date):
    self.__drive = Drive(scheme)
    self.__file = self.__drive.read("%s %s.json" % (date, scheme))
  
  def code_list_list(self):
    results = []
    for item in self.__file['code_lists']:
      results.append({ 'identifier': item['conceptId'] })  
    print("CODE_LIST_LIST [1]:", results)
    return results
