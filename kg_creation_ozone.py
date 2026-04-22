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

data = io.csv_to_dict(ateco_csv_filepath)
for i, item in enumerate(data):
    if i >= 5: break
    print(json.dumps(item, indent=4))
