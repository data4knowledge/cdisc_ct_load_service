import requests
import os

API_KEY = os.getenv('CDISC_API_KEY')
BASE_URL = "https://api.library.cdisc.org/api/"

class CtApi():

  def __init__(self, package, date):
    self.__package = package
    self.__date = date
  
  def read(self):
    return self.api_get("mdr/ct/packages/%s-%s/codelists" % (self.__package, self.__date))

  def api_get(self, url):
    api_url = "https://api.library.cdisc.org/api/%s" % (url)
    headers =  {"Content-Type":"application/json", "api-key": API_KEY}
    response = requests.get(api_url, headers=headers)
    return response
