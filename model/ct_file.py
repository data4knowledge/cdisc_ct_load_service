from datetime import datetime
from drive.drive import Drive

class CtFile():

  def __init__(self, scheme, date):
    self.__drive = Drive(scheme)
    self.scheme = scheme
    self.date = date
  
  def filename(self):
    return "%s %s.json" % (self.date, self.scheme)

  def read(self):
    self.__file = self.__drive.read(self.filename())

  def code_list_list(self):
    results = []
    filename = self.filename()
    for item in self.__file['codelists']:
      results.append({ 'identifier': item['conceptId'], 'filename': filename })  
    print("CODE_LIST_LIST [1]:", results)
    return results
