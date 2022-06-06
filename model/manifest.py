from datetime import date, datetime
from drive.drive import Drive

class Manifest():

  def __init__(self):
    self.__drive = Drive()
    self.__manifest = self.__drive.read('manifest', 'manifest.yaml')
  
  def next_after(self, this_date):
    dates = {}
    for date_str in self.__manifest.keys():
      manifest_date = datetime.strptime(date_str, '%Y-%m-%d').date()
      diff = manifest_date - this_date
      if diff.days > 0:
        dates[diff.days] = manifest_date
    return dates[min(dates.keys())]
