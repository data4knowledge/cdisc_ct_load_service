from fastapi import FastAPI

VERSION = "0.1"
SYSTEM_NAME = "d4k CT Load Microservice"

app = FastAPI()

@app.get("/")
def read_root():
  return { 'version': VERSION, 'system': SYSTEM_NAME }

@app.post("/configuration")
def create_configuration():
  return { 'status': 'ok' }

# @app.post("/namespace")
# async def create_namespace(namespace: NamespacePost):
#   return namespace.save()

# @app.get("/namespace/{uuid}")
# def read_namespace(uuid: UUID):
#   return NamespaceGet.read(uuid)

# @app.get("/namespace")
# def list_namespace():
#   return NamespaceGet.list()

