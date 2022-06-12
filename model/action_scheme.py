from model.action import Action
from model.action_code_list import ActionCodeList
from model.ct_api import CtApi
from model.ct_file import CtFile
from drive.drive import Drive
from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.skos_concept_scheme import SkosConceptScheme

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
    cs = SkosConceptScheme(label = "CDISC")
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    self.__repo.save(cs, si, rs, sv)
    list = self.code_list_list()
    return [ActionCodeList(**i).preserve() for i in list]

  #def to_preserve(self):
  #  return { 'scheme': self.scheme, 'date': self.date, 'format': self.format }
  
  def code_list_list(self):
    print("CODE_LIST_LIST: %s, %s" % (self.scheme, self.date))
    if self.format == "api":
      api = CtApi(self.scheme, self.date)
      data = api.read()
      Drive(self.scheme).upload(data)
    file = CtFile(self.scheme, self.date)
    return file.code_list_list()


