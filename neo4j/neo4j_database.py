from py2neo.ogm import Repository
import os

class Neo4jDatabase():
  
  def __init__(self):
    url = os.environ['CDISC_CT_LOAD_SERVICE_NEO4J_URL']
    usr = os.environ['CDISC_CT_LOAD_SERVICE_NEO4J_USER']
    pwd = os.environ['CDISC_CT_LOAD_SERVICE_NEO4J_PWD']
    self.__repo = Repository(url, name="neo4j", user=usr, password=pwd)

  def repository(self):
    return self.__repo

  def graph(self):
    return self.__repo.graph