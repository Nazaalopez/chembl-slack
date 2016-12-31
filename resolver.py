import re
from chembl_webresource_client.utils import utils
from chembl_webresource_client.unichem import UniChemClient

from chembl_webresource_client.settings import Settings
Settings.Instance().TOTAL_RETRIES = 1
Settings.Instance().TIMEOUT = 0.5
Settings.Instance().NEW_CLIENT_TIMEOUT = 0.5

inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')
smilesRegex = re.compile(r'^([^J][.0-9BCGOHMNSEPRIFTLUA@+\-\[\]\(\)\\\/%=#$]+)$')

class CorrectedUniChemClient(UniChemClient):
    def get(self, pk, src_id=None, to_src_id=None, all=False, url=False, verbose=False):
        #if pk.upper().startswith('CHEMBL'):
        #    url = '{0}/src_compound_id/{1}/1'.format(self.base_url, pk)
        #elif inchi_key_regex.match(pk):
        #    url = '{0}/inchikey/{1}'.format(self.base_url, pk)
        #else:
        url = '{0}/orphanIdMap/{1}'.format(self.base_url, pk)
        try:
            return self._get_results(url)
        except:
            return None

unichem = CorrectedUniChemClient()    
    
def resolve(mystery):
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
            return {int(x['src_id']):x['src_compound_id'] for x in ret}
        except TypeError:
            return {int(x['src_id']):x['src_compound_id'] for x in ret.items()[0][1]}
    return False
