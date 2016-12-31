import re
from chembl_webresource_client.utils import utils
from chembl_webresource_client.new_client import new_client
from chembl_webresource_client.unichem import UniChemClient

from chembl_webresource_client.settings import Settings
Settings.Instance().TOTAL_RETRIES = 1
Settings.Instance().TIMEOUT = 0.5
Settings.Instance().NEW_CLIENT_TIMEOUT = 0.5

molecule = new_client.molecule
molecule.set_format('json')
chembl_id_lookup = new_client.chembl_id_lookup
chembl_id_lookup.set_format('json')

inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')
smilesRegex = re.compile(r'^([^J][.0-9BCGOHMNSEPRIFTLUA@+\-\[\]\(\)\\\/%=#$]+)$')

class CorrectedUniChemClient(UniChemClient):
    def get(self, pk, src_id=None, to_src_id=None, all=False, url=False, verbose=False):
        if inchi_key_regex.match(pk):
            url = '{0}/inchikey/{1}'.format(self.base_url, pk)
        else:    
            url = '{0}/orphanIdMap/{1}'.format(self.base_url, pk)
        try:
            return self._get_results(url)
        except:
            return None

unichem = CorrectedUniChemClient()    
    
def resolve(mystery):
    if mystery.startswith('CHEMBL') or inchi_key_regex.match(mystery):
        ret = molecule.get(mystery)
        if ret:
            return ret
        ret = chembl_id_lookup(mystery)
        if ret:
            return ret['entity_type']
    inchi_key = None
    if inchi_key_regex.match(mystery.upper()):
        inchi_key = mystery
    elif smilesRegex.match(mystery.upper()):
        inchi_key = utils.inchi2inchiKey(utils.ctab2inchi(utils.smiles2ctab(mystery)))
    elif mystery.upper().startswith('INCHI='):
        inchi_key = utils.inchi2inchiKey(mystery)
    if inchi_key:
        ret = unichem.get(inchi_key)
    else:
        ret = unichem.get(mystery)
    if ret:
        try:
            mappings = {int(x['src_id']):x['src_compound_id'] for x in ret}
        except TypeError:
            mappings = {int(x['src_id']):x['src_compound_id'] for x in ret.items()[0][1]}
        if mappings.get(1):
            return molecule.get(mappings.get(1))
    else:
        ret = molecule.search(mystery)
        if len(ret):
            return ret[0]
    return False
