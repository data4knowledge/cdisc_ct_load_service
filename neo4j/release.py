from py2neo.ogm import Model, Property, RelatedTo
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus

class Release(Model):
  label = Property()
  identified_by = RelatedTo(ScopedIdentifier, "IDENTIFIED_BY")
  has_status = RelatedTo(RegistrationStatus, "HAS_STATUS")
  previous = RelatedTo('SkosConceptScheme', "PREVIOUS")