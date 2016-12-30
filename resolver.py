import re
from chembl_webresource_client.utils import utils

inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')
smilesRegex = re.compile(r'^([^J][.0-9BCGOHMNSEPRIFTLUA@+\-\[\]\(\)\\\/%=#$]+)$')

def resolve(mystery):
  if smilesRegex.match(mystery.upper()):
    return utils.inchi2inchiKey(utils.ctab2inchi(utils.smiles2ctab(mystery)))
  elif mystery.upper().startswith('INCHI='):
    return utils.inchi2inchiKey(mystery)
  return False
