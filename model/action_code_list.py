from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from model.ct_file import CtFile
from store.store import Store
from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.skos_concept import SkosConcept

class ActionCodeList(Action):
  identifier: str
  filename: str

  def __init__(self, *args, **kwargs):
    self.identifier = kwargs.pop('identifier')
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    sv = SemanticVersion(major="1", minor="0", patch="0")
    si = ScopedIdentifier(version = "1", version_label = self.date, identifier = "%s" % (self.identifier))
    si.semantic_version.add(sv)
    rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
    file = CtFile(self.scheme, self.date)
    file.read()
    codelist = file.code_list(self.identifier)
    print("ACTIONCODELIST.PROCESS [1]:", codelist)
    synonyms = []
    if 'synonyms' in codelist:
      synonyms = codelist['synonyms']
    cs = SkosConcept(label = codelist['name'],
      identifier = self.identifier,
      notation = codelist['submissionValue'],
      #alt_label = synonyms,
      pref_label = codelist['preferredTerm'],
      definition = codelist['definition']
    )
    print("ACTIONCODELIST.PROCESS [2]:", vars(cs))
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    for cl in codelist['terms']:
      synonyms = []
      if 'synonyms' in codelist:
        synonyms = codelist['synonyms']
      child = SkosConcept(label = cl['preferredTerm'],
        identifier = cl['conceptId'],
        notation = cl['submissionValue'],
        #alt_label = synonyms,
        pref_label = cl['preferredTerm'],
        definition = cl['definition']
      )
      cs.narrower.add(child)
    self.__repo.save(cs)  
    return []
