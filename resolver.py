import re
from chembl_webresource_client.utils import utils
from chembl_webresource_client.unichem import unichem_client as unichem
from chembl_webresource_client.unichem import UniChemClient

inchi_key_regex = re.compile('[A-Z]{14}-[A-Z]{10}-[A-Z]')
smilesRegex = re.compile(r'^([^J][.0-9BCGOHMNSEPRIFTLUA@+\-\[\]\(\)\\\/%=#$]+)$')

class CorrectedUniChemClient(UniChemClient):
    def get(self, pk, src_id=None, to_src_id=None, all=False, url=False, verbose=False):
        if pk.upper().startswith('CHEMBL'):
            if to_src_id:
                if url:
                    url = '{0}/src_compound_id_url/{1}/{2}/{3}'.format(self.base_url, pk, src_id, to_src_id)
                elif all:
                    url = '{0}/src_compound_id_all/{1}/{2}/{3}'.format(self.base_url, pk, src_id, to_src_id)
                else:
                    url = '{0}/src_compound_id/{1}/{2}/{3}'.format(self.base_url, pk, src_id, to_src_id)
            else:
                if all:
                    url = '{0}/src_compound_id_all/{1}/{2}'.format(self.base_url, pk, src_id)
                else:
                    url = '{0}/src_compound_id/{1}/{2}'.format(self.base_url, pk, src_id)
        elif inchi_key_regex.match(pk):
            if all:
                url = '{0}/inchikey_all/{1}'.format(self.base_url, pk)
            elif verbose:
                url = '{0}/verbose_inchikey/{1}'.format(self.base_url, pk)
            else:
                url = '{0}/inchikey/{1}'.format(self.base_url, pk)
        else:
            if to_src_id:
                url = '{0}/src_compound_id_all_obsolete/{1}/{2}/{3}'.format(self.base_url, pk, src_id, to_src_id)
            else:
                if src_id:
                    url = '{0}/src_compound_id_all_obsolete/{1}/{2}'.format(self.base_url, pk, src_id)
                else:
                    url = '{0}/orphanIdMap/{1}'.format(self.base_url, pk) 
        return self._get_results(url)

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
