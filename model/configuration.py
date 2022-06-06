from pydantic import BaseModel
from datetime import date

class Configuration(BaseModel):
  start_date: date
  