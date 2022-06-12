from py2neo.ogm import Model, Property, RelatedTo
from neo4j.concept import Concept

class SkosConcept(Concept):
  identifier: Property()
  notation: Property()
  atl_label: Property()
  pre_label: Property()
  definition: Property()

  previous = RelatedTo('SkosConcept', "PREVIOUS")
  narrower = RelatedTo('SkosConcept', "NARROWER")
 