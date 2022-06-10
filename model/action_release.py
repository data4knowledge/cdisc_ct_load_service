from model.action import Action
from model.action_scheme import ActionScheme
from model.configuration import Configuration
from model.manifest import Manifest
from store.store import Store
from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.release import Release

class ActionRelease(Action):
  release_date: str

  def __init__(self, *args, **kwargs):
    print("ID:", args)
    print("KW:", kwargs)
    self.release_date = kwargs.pop('release_date')
    self.__manifest = Manifest()
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()
    #super().__init__(*args, **kwargs)
    
  def process(self):
    sv = SemanticVersion(major="1", minor="0", patch="0")
    si = ScopedIdentifier(version = "1", version_label = self.release_date, identifier = "CT")
    si.semantic_version.add(sv)
    rs = RegistrationStatus(registration_status = "Released", effective_date = self.release_date, until_date = "")
    rel = Release(label = "Controlled Terminology")
    rel.has_status.add(rs)
    rel.identified_by.add(si)
    self.__repo.save(rel, rs, si, sv)
    list = self.__manifest.concept_scheme_list(self.release_date)
    return [ActionScheme(**i).preserve() for i in list]

  def to_preserve(self):
    return { 'release_date': self.release_date }