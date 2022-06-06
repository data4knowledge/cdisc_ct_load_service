from typing import List, Union
from pydantic import validator
import json

class Company(BaseModel):
  start_date: date
  
  @classmethod
  def check_code(cls, code):
    f = open('data/country.json')
    codes = json.load(f)
    return next((item for item in codes if item["alpha-3"] == code), None)
  
  @validator('country_code')
  def code_must_be_valid(cls, code):
    if cls.check_code(code) == None:
      raise ValueError('must ba a valid ISO 3166 code')
    return code

