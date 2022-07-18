from py2neo.ogm import Model, Property, RelatedTo
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.extension import Extension
from neo4j.neo4j_database import Neo4jDatabase

class Concept(Model):
  uuid = Property()
  uri = Property()
  label = Property()
  
  identified_by = RelatedTo(ScopedIdentifier, "IDENTIFIED_BY")
  has_status = RelatedTo(RegistrationStatus, "HAS_STATUS")
  previous = RelatedTo('Concept', "PREVIOUS")
  extended_with = RelatedTo(Extension, "EXTENDED_WITH")

  def version(self):
    for item in self.identified_by:
      return int(item.version)
    return None

  @classmethod
  def latest(cls, identifier):
    db = Neo4jDatabase()
    query = """
      MATCH (a)-[:IDENTIFIED_BY]->(si) WHERE si.identifier='%s' AND NOT ()-[:PREVIOUS]->(a) RETURN a
    """ % (identifier)
    #print("CONCEPT.LATEST [1]: %s" % (query))
    results = db.graph().run(query).data()
    if len(results) == 0:
      return None
    return cls.wrap(results[0]['a'])

  def dict(self):
    #print("Node: ", dict(self.__ogm__.node))
    return dict(self.__ogm__.node)