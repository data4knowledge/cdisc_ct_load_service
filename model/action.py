class Action():
  
  def to_store(self):
    return { 'klass': self.__class__.__name__, 'data': self.to_json()}

  # def set_releases(self):
  #   self.releases = self.__manifest.release_list(self.start_date)
  #   self.__store.put(RELEASE, json.dumps([self._to_iso8601_str(i) for i in self.releases]))

  # def set_thesauri(self):
  #   self.code_lists = [] # To come
  #   self.__store.put(THESAURUS, json.dumps(self.thesauri))

  # def set_code_lists(self):
  #   self.code_lists = [] # To come
  #   self.__store.put(CODE_LIST, json.dumps(self.code_lists))

  # def _read_release(self):
  #   data = self.__store.get(RELEASE)
  #   if data == None:
  #     self.releases = []
  #   else:
  #     data = json.loads(data)
  #     self.releases = [self._from_iso8601_str(i) for i in data]
    
  # def _read_thesauri(self):
  #   data = self.__store.get(THESAURUS)
  #   if data == None:
  #     self.thesauri = []
  #   else:
  #     self.thesauri = json.loads(data)

  # def _read_code_lists(self):
  #   data = self.__store.get(CODE_LIST)
  #   if data == None:
  #     self.code_lists = []
  #   else:
  #     self.code_lists = json.loads(data)
    
  # def _from_iso8601_str(self, text):
  #   return datetime.strptime(text, '%Y-%m-%d').date()
  
  # def _to_iso8601_str(self, date):
  #   return date.strftime("%Y-%m-%d")
