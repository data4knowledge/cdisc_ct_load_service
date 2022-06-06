from datetime import date, datetime
from drive.drive import Drive

class Manifest():

  def __init__(self):
    self.__drive = Drive()
    self.__manifest = self.__drive.read('manifest', 'manifest.yaml')
  
  def next_release_after(self, this_date):
    dates = {}
    for date_str in self.__manifest.keys():
      manifest_date = self._from_iso8601_str(date_str)
      diff = manifest_date - this_date
      if diff.days > 0:
        dates[diff.days] = manifest_date
    return dates[min(dates.keys())]

  def release_list(self, start_date):
    releases = []
    for date_str in self.__manifest.keys():
      manifest_date = self._from_iso8601_str(date_str)
      diff = manifest_date - start_date
      if diff.days > 0:
        releases.append(manifest_date)
    return releases

  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()
