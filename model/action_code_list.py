from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from model.ct_file import CtFile
from model.ct_api import CtApi
from store.store import Store
from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.skos_concept import SkosConcept
from neo4j.skos_concept_scheme import SkosConceptScheme
from uuid import uuid4
import os
from deepdiff import DeepDiff

class ActionCodeList(Action):
  identifier: str
  scheme: str
  date: str
  parent_uri: str

  def __init__(self, *args, **kwargs):
    self.identifier = kwargs.pop('identifier')
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.parent_uri = kwargs.pop('parent_uri')
    self.format = kwargs.pop('format')
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    previous_items = {}
    previous_dicts = {}
    scs = SkosConceptScheme.match(self.__db.graph()).where(uri=self.parent_uri).first()
    previous = SkosConcept.latest(self.identifier)
    if previous == None:
      version = "1"
      previous_dict = None
    else:
      version = "%s" % (previous.version() + 1)
      previous_dict = previous.dict()
      previous_dict.pop('uuid')
      previous_dict.pop('uri')
      previous_dict['terms'] = []
      for item in previous.narrower:
        item_dict = item.dict()
        item_dict.pop('uuid')
        item_dict.pop('uri')
        previous_dict['terms'].append(item_dict)
        previous_items[item.identifier] = item
        previous_dicts[item.identifier] = item_dict

    print("ACTIONCODELIST.PROCESS [2]: next version = %s" % (version))
    #print("ACTIONCODELIST.PROCESS [3a]: %s" % (previous_dict))    
    print("ACTIONCODELIST.PROCESS [3b]: %s" % (previous_items))    

    if self.format == "api":
      api = CtApi(self.scheme, self.date)
      codelist = api.read_code_list(self.identifier)
      print("ACTIONCODELIST.PROCESS [4a]:", codelist['conceptId'])
    else:
      file = CtFile(self.scheme, self.date)
      file.read()
      codelist = file.code_list(self.identifier)
      print("ACTIONCODELIST.PROCESS [4b]:", codelist['conceptId'])

    codelist.pop('extensible')
    codelist.pop('conceptId')
    codelist['identifier'] = self.identifier
    codelist['label'] = codelist.pop('name')
    codelist['notation'] = codelist.pop('submissionValue')
    codelist['pref_label'] = codelist.pop('preferredTerm')
    if 'synonyms' in codelist:
      codelist['alt_label'] = codelist.pop('synonyms')
    else:
      codelist['alt_label'] = []
    for term in codelist['terms']:
      term['identifier'] = term.pop('conceptId')
      term['label'] = term['preferredTerm']
      term['notation'] = term.pop('submissionValue')
      term['pref_label'] = term.pop('preferredTerm')
      if 'synonyms' in term:
        term['alt_label'] = term.pop('synonyms')
      else:
        term['alt_label'] = []
    print("ACTIONCODELIST.PROCESS [5a]: %s" % (codelist))
    print("ACTIONCODELIST.PROCESS [5b]: %s" % (DeepDiff(previous_dict, codelist, ignore_order=True)))
    if (previous_dict == None) or (not previous_dict == None and DeepDiff(previous_dict, codelist, ignore_order=True)):
      sv = SemanticVersion(major=version, minor="0", patch="0")
      si = ScopedIdentifier(version = version, version_label = self.date, identifier = "%s" % (self.identifier))
      si.semantic_version.add(sv)
      rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")

      uuid = str(uuid4())
      uri = "%scdisc/ct/sc/%s/%s/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], self.date, self.scheme, self.identifier)
      cs = SkosConcept(label = codelist['label'],
        identifier = codelist['identifier'],
        notation = codelist['notation'],
        alt_label = codelist['alt_label'],
        pref_label = codelist['pref_label'],
        definition = codelist['definition'],
        uuid = uuid,
        uri = uri
      )
      if not previous == None:
        cs.previous.add(previous)
      scs.top_level_concept.add(cs)
      #print("ACTIONCODELIST.PROCESS [2]")
      cs.identified_by.add(si)
      cs.has_status.add(rs)
      for cl in codelist['terms']:
        if cl['identifier'] in previous_items:
          previous_term = previous_items[cl['identifier']]
          the_dict = previous_dicts[cl['identifier']]
        else:
          previous_term = None
          the_dict = None
        if previous_term != None:
          print("ACTIONCODELIST.PROCESS [6b]: ", the_dict)
          print("ACTIONCODELIST.PROCESS [6b]: ", cl)
          differences = DeepDiff(the_dict, cl, ignore_order=True)
          diff = differences != {}
          print("ACTIONCODELIST.PROCESS [6c]: ", diff)
          print("ACTIONCODELIST.PROCESS [6d]: ", DeepDiff(the_dict, cl, ignore_order=True))
        else:
          print("ACTIONCODELIST.PROCESS [6e]: ")
          diff = True
        if diff:  
          uuid = str(uuid4())
          uri = "%scdisc/ct/sc/%s/%s/%s/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], self.date, self.scheme, self.identifier, cl['identifier'])
          child = SkosConcept(label = cl['label'],
            identifier = cl['identifier'],
            notation = cl['notation'],
            alt_label = cl['alt_label'],
            pref_label = cl['pref_label'],
            definition = cl['definition'],
            uuid = uuid,
            uri = uri
          )
          if previous_term != None:
            child.previous.add(previous_term)
        else:
          child = previous_term
        #print("ACTIONCODELIST.PROCESS [5]: ", child)
        cs.narrower.add(child)
      self.__repo.save(cs, scs)
    else:
      scs.top_level_concept.add(previous)
      self.__repo.save(scs)
    #print("ACTIONCODELIST.PROCESS [5]:")
    return []

  def search(self, items, identifier):
    print("ACTIONCODELIST.SEARCH [1]: %s, %s" % (items, identifier))
    if items == None:
      return None
    for p in items['terms']:
      print("ACTIONCODELIST.SEARCH [2]: %s" % (p))
      if p['identifier'] == identifier:
        return p
    print("ACTIONCODELIST.SEARCH [3]: None")
    return None