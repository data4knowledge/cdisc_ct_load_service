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
from neo4j.skos_concept_scheme import SkosConceptScheme
from uuid import uuid4
import os

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
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    scs = SkosConceptScheme.match(self.__db.graph()).where(uri=self.parent_uri).first()
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
    uuid = str(uuid4())
    uri = "%scdisc/ct/sc/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], uuid)
    cs = SkosConcept(label = codelist['name'],
      identifier = self.identifier,
      notation = codelist['submissionValue'],
      alt_label = synonyms,
      pref_label = codelist['preferredTerm'],
      definition = codelist['definition'],
      uuid = uuid,
      uri = uri
    )
    scs.top_level_concept.add(cs)
    print("ACTIONCODELIST.PROCESS [2]:", vars(cs))
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    for cl in codelist['terms']:
      synonyms = []
      if 'synonyms' in codelist:
        synonyms = codelist['synonyms']
      uuid = str(uuid4())
      uri = "%scdisc/ct/sc/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], uuid)
      child = SkosConcept(label = cl['preferredTerm'],
        identifier = cl['conceptId'],
        notation = cl['submissionValue'],
        alt_label = synonyms,
        pref_label = cl['preferredTerm'],
        definition = cl['definition'],
        uuid = uuid,
        uri = uri
      )
      cs.narrower.add(child)
    self.__repo.save(cs, scs)  
    return []
