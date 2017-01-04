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
