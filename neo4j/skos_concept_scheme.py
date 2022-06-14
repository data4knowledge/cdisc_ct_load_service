from py2neo.ogm import Model, Property, RelatedTo
from neo4j.concept import Concept
from neo4j.skos_concept import SkosConcept

class SkosConceptScheme(Concept):
  top_level_concept = RelatedTo(SkosConcept, "TOP_LEVEL_CONCEPT")