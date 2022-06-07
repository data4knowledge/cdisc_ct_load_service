class Action():

  def __init__(self, config):
    self.__config = config

  def next(self):
    cl = self.__config.next_code_list()
    if cl == None:
      cs = self.__config.next_concept_scheme()
      if cs == None:
        rel = self.__config.next_release()
        if rel == None:
          return None
        else:
          self.__config.move_to_next_release()
      else:
        self.__config.move_to_next_concept_scheme()
    else:
      self._process_concept_set()
    