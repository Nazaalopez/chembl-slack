import time

MESSAGE_TEMPLATE = {
    "attachments": [
        {
            "fallback": "Compound Report Card",
            "color": "#009688",
            "pretext": "Compound Report Card",
            "author_name": "",
            "title": "",
            "title_link": "https://chembl-glados.herokuapp.com/compound_report_card/{0}/",
            "text": "",
            "fields": [
                {
                    "title": "Max Phase",
                    "value": "",
                    "short": True
                },
                {
                    "title": "Molecular Formula",
                    "value": "",
                    "short": True
                },
                {
                    "title": "Canonical SMILES",
                    "value": "",
                    "short": False
                },
                {
                    "title": "Standard InChI",
                    "value": "",
                    "short": False
                }				
            ],
            "image_url": "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=500",
            "thumb_url": "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=50",
            "footer": "ChEMBL API",
            "footer_icon": "https://avatars0.githubusercontent.com/u/3062531?v=3&s=70",
            "ts": None
        }
    ]
}

def render(context):
    msg = MESSAGE_TEMPLATE.copy()
    chembl_id = context["molecule_chembl_id"]
    msg["attachments"][0]["author_name"] = context["pref_name"]
    msg["attachments"][0]["title"] = chembl_id
    msg["attachments"][0]["title_link"] = "https://chembl-glados.herokuapp.com/compound_report_card/{0}/".format(chembl_id)
    msg["attachments"][0]["image_url"] = "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=500".format(chembl_id)
    msg["attachments"][0]["thumb_url"] = "https://www.ebi.ac.uk/chembl/api/data/image/{0}.png?engine=indigo&ignoreCoords=1&dimensions=50".format(chembl_id)
    msg["attachments"][0]["text"] = context["molecule_structures"]["standard_inchi_key"]
    msg["attachments"][0]["fields"][0]["value"] = context["max_phase"]
    msg["attachments"][0]["fields"][1]["value"] = context["molecule_properties"]["full_molformula"]
    msg["attachments"][0]["fields"][2]["value"] = context["molecule_structures"]["canonical_smiles"]
    msg["attachments"][0]["fields"][3]["value"] = context["molecule_structures"]["standard_inchi"]
    msg["attachments"][0]["ts"] = int(time.time())
    return msg
