import json


import json

class Action():
  
  def __init__(self, *initial_data, **kwargs):
    for dictionary in initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])

  def preserve(self):
    return { 'klass': self.__class__.__name__, 'data': json.dumps(self.__dict__)}
