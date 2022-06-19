from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.release import Release

db = Neo4jDatabase()
repo = db.repository()
graph = db.graph()
graph.delete_all()

a = SemanticVersion(major="10", minor="0", patch="0")
b = ScopedIdentifier(version = "10", version_label = "2021-01-01", identifier = "CT")
b.semantic_version.add(a)
c = RegistrationStatus(registration_status = "draft", effective_date = "2021-01-01", until_date = "")
e = Release(label = "CDISC")
e.has_status.add(c)
e.identified_by.add(b)
repo.save(e)


a = SemanticVersion(major="11", minor="0", patch="0")
b = ScopedIdentifier(version = "11", version_label = "2022-01-01", identifier = "CT")
b.semantic_version.add(a)
c = RegistrationStatus(registration_status = "draft", effective_date = "2022-01-01", until_date = "")
d = Release(label = "CDISC")
d.has_status.add(c)
d.identified_by.add(b)
d.previous.add(e)
repo.save(d)

x = Release.latest("CT")
print(x, type(x))
#y = Release.wrap(x)
#print(y, type(y))

a = SemanticVersion(major="12", minor="0", patch="0")
b = ScopedIdentifier(version = "12", version_label = "2022-02-02", identifier = "CT")
b.semantic_version.add(a)
c = RegistrationStatus(registration_status = "draft", effective_date = "2022-02-02", until_date = "")
d = Release(label = "CDISC")
d.has_status.add(c)
d.identified_by.add(b)
d.previous.add(x)
repo.save(d)