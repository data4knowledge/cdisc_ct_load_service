from py2neo.ogm import Model, Property, RelatedTo
from neo4j.concept import Concept

class SkosConcept(Concept):
  identifier = Property()
  notation = Property()
  alt_label = Property()
  pref_label = Property()
  definition = Property()

  narrower = RelatedTo('SkosConcept', "NARROWER")
 