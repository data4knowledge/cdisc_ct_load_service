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
from neo4j.release import Release
from uuid import uuid4
import json
import os

class ActionScheme(Action):
  scheme: str
  date: str
  format: str
  parent_uri: str

  def __init__(self, *args, **kwargs):
    print("ACTION_SCHEME.__INIT__: %s" % (kwargs))
    self.scheme = kwargs.pop('scheme')
    self.date = kwargs.pop('date')
    self.format = kwargs.pop('format')
    self.parent_uri = kwargs.pop('parent_uri')
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    sr = Release.match(self.__db.graph()).where(uri=self.parent_uri).first()
    sv = SemanticVersion(major="1", minor="0", patch="0")
    si = ScopedIdentifier(version = "1", version_label = self.date, identifier = "%s CT" % (self.scheme))
    si.semantic_version.add(sv)
    rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
    uuid = str(uuid4())
    uri = "%scdisc/ct/cs/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], uuid)
    cs = SkosConceptScheme(label = self.scheme, uuid = uuid, uri = uri)
    cs.has_status.add(si)
    cs.identified_by.add(rs)
    sr.consists_of.add(cs)
    self.__repo.save(cs, si, rs, sv, sr)
    list = self.code_list_list()
    for i in list:
      i['parent_uri'] = uri
    return [ActionCodeList(**i).preserve() for i in list]

  def code_list_list(self):
    print("CODE_LIST_LIST [1]: %s, %s" % (self.scheme, self.date))
    if self.format == "api":
      drive = Drive(self.scheme)
      filename = CtFile(self.scheme, self.date).filename()
      print("CODE_LIST_LIST [2]: %s" % (filename))
      if not drive.present(filename):
        print("CODE_LIST_LIST [3]: Not present")
        api = CtApi(self.scheme, self.date)
        data = api.read()
        Drive(self.scheme).upload(filename, json.dumps(data))
    file = CtFile(self.scheme, self.date)
    file.read()
    return file.code_list_list()


