from neo4j.neo4j_database import Neo4jDatabase
from neo4j.semantic_version import SemanticVersion
from neo4j.scoped_identifier import ScopedIdentifier
from neo4j.registration_status import RegistrationStatus
from neo4j.release import Release

db = Neo4jDatabase()
repo = db.repository()
graph = db.graph()
graph.delete_all()

a = SemanticVersion(major="11", minor="0", patch="0")
b = ScopedIdentifier(version = "11", version_label = "2022-01-01", identifier = "CT")
b.semantic_version.add(a)
c = RegistrationStatus(registration_status = "draft", effective_date = "2022-01-01", until_date = "")
d = Release(label = "CDISC")
d.has_status.add(c)
d.identified_by.add(b)
repo.save(a, b, c, d)
