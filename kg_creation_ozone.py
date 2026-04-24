import json

import pandas as pd

from lib import io

proj_name = 'ozone'
proj_folderpath = f'C:\\engineering\\projects\\{proj_name}'
kg_folderpath = f'{proj_folderpath}/kg'
naics_folderpath = f'{kg_folderpath}/naics'
naics_data_filepath = f'{naics_folderpath}/2022_NAICS_Structure.xlsx'

ateco_folderpath = f'{kg_folderpath}/ateco'
ateco_xlsx_filepath = f'{ateco_folderpath}/StrutturaATECO-2025-IT-EN-1.xlsx'
ateco_csv_filepath = f'{ateco_folderpath}/StrutturaATECO-2025-IT-EN-1.csv'

def naics_xlsx_to_json():
    df = pd.read_excel(naics_data_filepath)
    df = df.iloc[2:].reset_index(drop=True)
    rows = df.to_dict(orient='records')
    rows = []
    for _, row in df.iterrows():
        code = row[1]
        code_len = len(str(code))
        try: name = row[2].strip()
        except: continue
        ###
        hierarchy = ''
        if code_len == 2: hierarchy = 'sector'
        elif code_len == 3: hierarchy = 'subsector'
        elif code_len == 4: hierarchy = 'industry group'
        elif code_len == 5: hierarchy = 'NAICS industries'
        elif code_len == 6: hierarchy = 'U.S. detail'
        item = {
            'hierarchy': hierarchy,
            'code': code,
            'name': name,
        }
        rows.append(item)
    with open(f'{naics_folderpath}/data.json', 'w') as f:
        json.dump(rows, f, indent=4)

def ateco_csv_to_json():
    data = io.csv_to_dict(ateco_csv_filepath)
    output_data = []
    for i, item in enumerate(data):
        print(json.dumps(item, indent=4))
        item = {
            'node_i': item['ORDINE_CODICE_ATECO_2025'],
            'node_id': item['CODICE_ATECO_2025'],
            'node_title_italian': item['TITOLO_ITALIANO_ATECO_2025'],
            'node_title_english': item['TITOLO_INGLESE_ATECO_2025'],
            'node_rank': item['GERARCHIA_ATECO_2025'],
            'parent_id': item['CODICE_PADRE_ATECO_2025'],
            'parent_rank': item['GERARCHIA_PADRE_ATECO_2025'],
        }
        output_data.append(item)
    with open(f'{ateco_folderpath}/data.json', 'w') as f:
        json.dump(output_data, f, indent=4)

# industrial ontology foundry (facilities) | industry -> facility
def iof_lib_to_json():
    from ontolearner.ontology import IOF
    ontology = IOF()
    ontology.load(f'{kg_folderpath}/iof/ontology-Release_202601/core/Core.rdf')
    data = ontology.extract()
    # print(json.dumps(data, indent=4))
    term_types = data.term_typings
    taxonomic_relationships = data.type_taxonomies
    non_taxonomic_relationships = data.type_non_taxonomic_relations

    for x in term_types:
        print(x)
    print('--------------------------------------------')
    for x in taxonomic_relationships:
        print(x)
    print('--------------------------------------------')
    for x in non_taxonomic_relationships:
        print(x)


def ontolearner_agro():
    from ontolearner import AgrO
    ontology = AgrO()
    ontology.load()
    ontological_data = ontology.extract()
    print(ontological_data)

# ateco_csv_to_json()
# iof_lib_to_json()
ontolearner_agro()
