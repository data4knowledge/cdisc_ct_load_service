from py2neo.ogm import Model, Property, RelatedTo
#from neo4j.concept import Concept
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus

class SkosConcept(Model):
  label = Property()
  identifier = Property()
  notation = Property()
  alt_label = Property()
  pref_label = Property()
  definition = Property()

  identified_by = RelatedTo(ScopedIdentifier, "IDENTIFIED_BY")
  has_status = RelatedTo(RegistrationStatus, "HAS_STATUS")
  previous = RelatedTo('SkosConcept', "PREVIOUS")
  narrower = RelatedTo('SkosConcept', "NARROWER")
 