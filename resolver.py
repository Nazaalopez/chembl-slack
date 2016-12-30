import re
from chembl_webresource_client.utils import utils
from chembl_webresource_client.unichem import unichem_client as unichem

inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')
smilesRegex = re.compile(r'^([^J][.0-9BCGOHMNSEPRIFTLUA@+\-\[\]\(\)\\\/%=#$]+)$')

def resolve(mystery):
  inchi_key = None
  if inchi_key_regex.match(mystery.upper()):
    inchi_key = mystery
  elif smilesRegex.match(mystery.upper()):
    inchi_key = utils.inchi2inchiKey(utils.ctab2inchi(utils.smiles2ctab(mystery)))
  elif mystery.upper().startswith('INCHI='):
    inchi_key = utils.inchi2inchiKey(mystery)
  if not inchi_key:
    return False
  ret = unichem.get(inchi_key)
  if ret:
    return {int(x['src_id']):x['src_compound_id'] for x in ret}
  return False
