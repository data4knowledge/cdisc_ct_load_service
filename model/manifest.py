from datetime import datetime
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
        dates[diff.days] = date_str
    return dates[min(dates.keys())]

  def release_list(self, start_date):
    releases = []
    start_date_as_date = self._from_iso8601_str(start_date)
    for date_str in self.__manifest.keys():
      #print("RELEASE_LIST [1]:", date_str)
      manifest_date = self._from_iso8601_str(date_str)
      diff = manifest_date - start_date_as_date
      #print("RELEASE_LIST [2]: %s v %s = %s" % (manifest_date, start_date, diff))
      if diff.days >= 0:
        releases.append(date_str)
    print("RELEASE_LIST [3]:", releases)
    return releases

  def concept_scheme_list(self, release_date):
    print("CONCEPT_SCHEME_LIST [1]:", release_date)
    print("CONCEPT_SCHEME_LIST [2]:", self.__manifest[release_date])
    results = []
    if "api" in self.__manifest[release_date]["format"]:
      format = "api"
    else:
      format = "file"
    for k, v in self.__manifest[release_date]["items"].items():
      results.append({ 'scheme': k, 'date': v, 'format': format })  
    print("CONCEPT_SCHEME_LIST [3]:", results)
    return results

  def _from_iso8601_str(self, text):
    return datetime.strptime(text, '%Y-%m-%d').date()

  def _to_iso8601_str(self, date):
    return date.strftime("%Y-%m-%d")