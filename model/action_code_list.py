from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
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
    self.filename = kwargs.pop('filename')
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    sv = SemanticVersion(major="1", minor="0", patch="0")
    si = ScopedIdentifier(version = "1", version_label = self.date, identifier = "%s" % (self.identifier))
    si.semantic_version.add(sv)
    rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
    cs = SkosConcept(label = self.identifier)
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    self.__repo.save(cs, si, rs, sv)
    # Process a single code list here

  #def to_preserve(self):
  #  return { 'filename': self.filename, 'identifier': self.identifier }
  

