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
    self.release_date = kwargs.pop('release_date')
    self.format = kwargs.pop('format')
    self.parent_uri = kwargs.pop('parent_uri')
    self.__db = Neo4jDatabase()
    self.__repo = self.__db.repository()

  def process(self):
    identifier = "%s CT" % (self.scheme.upper())
    sr = Release.match(self.__db.graph()).where(uri=self.parent_uri).first()
    previous = SkosConceptScheme.latest(identifier)
    if previous == None:
      version = "1"
    else:
      version = "%s" % (previous.version() + 1)
    print("ACTIONSCHEME.PROCESS [1]: next version = %s" % (version))
    # sv = SemanticVersion(major = version, minor="0", patch="0")
    # si = ScopedIdentifier(version = version, version_label = self.date, identifier = identifier)
    # si.semantic_version.add(sv)
    # rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
    # uuid = str(uuid4())
    # uri = "%scdisc/ct/cs/%s/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], self.date, self.scheme)
    # cs = SkosConceptScheme(label = self.scheme, uuid = uuid, uri = uri)
    # if not previous == None:
    #   cs.previous.add(previous)
    # cs.identified_by.add(si)
    # cs.has_status.add(rs)
    # sr.consists_of.add(cs)
    if self.release_date != self.date and previous != None:
      sr.consists_of.add(previous)
      self.__repo.save(sr)
      return []
    else:
      sv = SemanticVersion(major = version, minor="0", patch="0")
      si = ScopedIdentifier(version = version, version_label = self.date, identifier = identifier)
      si.semantic_version.add(sv)
      rs = RegistrationStatus(registration_status = "Released", effective_date = self.date, until_date = "")
      uuid = str(uuid4())
      uri = "%scdisc/ct/cs/%s/%s" % (os.environ["CDISC_CT_LOAD_SERVICE_BASE_URI"], self.date, self.scheme)
      cs = SkosConceptScheme(label = self.scheme, uuid = uuid, uri = uri)
      if not previous == None:
        cs.previous.add(previous)
      cs.identified_by.add(si)
      cs.has_status.add(rs)
      sr.consists_of.add(cs)
      self.__repo.save(cs, si, rs, sv, sr)
      list = self.code_list_list()
      print("ACTIONSCHEME.PROCESS [3]: %s" % (list))
      for i in list:
        i['parent_uri'] = uri
      return [ActionCodeList(**i).preserve() for i in list]

  def code_list_list(self):
    print("CODE_LIST_LIST [1]: %s, %s" % (self.scheme, self.date))
    if self.format == "api":
      #drive = Drive(self.scheme)
      #filename = CtFile(self.scheme, self.date).filename()
      #print("CODE_LIST_LIST [2]: %s" % (filename))
      #if not drive.present(filename):
      #  print("CODE_LIST_LIST [3]: Not present")
      results = []
      api = CtApi(self.scheme, self.date)
      for item in api.read_code_lists()['_links']['codelists']:

        # FOR TEST!!!
        #if item['conceptId'] != "C66741":
        #  continue
        identifier = item['href'].split("/")[-1]
        results.append({ 'identifier': identifier, 'scheme': self.scheme, 'date': self.date, 'format': "api" })  
      return results
      #  Drive(self.scheme).upload(filename, json.dumps(data))
    else:
      file = CtFile(self.scheme, self.date)
      file.read()
      return file.code_list_list()


