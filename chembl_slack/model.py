from chembl_webresource_client.settings import Settings
Settings.Instance().TOTAL_RETRIES = 1
Settings.Instance().BACKOFF_FACTOR = 0

import re
from chembl_webresource_client.utils import utils
from chembl_webresource_client.new_client import new_client
from chembl_webresource_client.unichem import UniChemClient

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
        ret = None
        try:
            ret = molecule.get(mystery)
        except:
            pass
        if ret:
            return 'COMPOUND', ret
        ret = chembl_id_lookup.get(mystery)
        if ret:
            if ret['status'].lower() == 'inactive':
                return False
            return ret['entity_type'], ret['chembl_id']
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
            try:
                return 'COMPOUND', molecule.get(mappings.get(1))
            except:
                pass
    else:
        ret = molecule.search(mystery)
        if len(ret):
            return 'COMPOUND', ret[0]
    return False
