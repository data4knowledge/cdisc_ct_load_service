import json

class Action():
  
  # def __init__(self, *initial_data, **kwargs):
  #   for dictionary in initial_data:
  #     for key in dictionary:
  #       setattr(self, key, dictionary[key])
  #   for key in kwargs:
  #     setattr(self, key, kwargs[key])

  def preserve(self):
    klass_name = self.__class__.__name__
    data = {}
    for k, v in vars(self).items():
      if not k.startswith("_%s" % (klass_name)):
        data[k] = v
        #print("PRESERVE [1]: %s = %s" % (k,v))
    result = { 'klass': klass_name, 'data': data}
    print("PRESERVE [2]:", result)
    return result
