from model.action import Action
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store
from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.concept_scheme import ConceptScheme

class ActionScheme(Action):
  scheme: str
  date: str
  format: str

  def __init__(self, *args, **kwargs):
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.format = kwargs.pop('format')
    #self.__store = Store("actions")
    #self.__manifest = Manifest()
    #self.__config = Configuration()
    #self.__actions = self.__store.get("list")
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()
    #super().__init__(*args, **kwargs)

  def process(self):
    sv = SemanticVersion(major="1", minor="0", patch="0")
    si = ScopedIdentifier(version = "1", version_label = self.date, identifier = "%s CT" % (self.scheme))
    si.semantic_version.add(sv)
    rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
    cs = ConceptScheme(label = "CDISC")
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    self.__repo.save(cs, si, rs, sv)

  def to_preserve(self):
    return { 'scheme': self.scheme, 'date': self.date }
  



