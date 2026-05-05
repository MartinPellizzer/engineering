import os
import json

from lib import io

vault_folderpath = f'C:\\vault'
ozonogroup_folderpath = f'{vault_folderpath}/ozonogroup'
database_folderpath = f'{ozonogroup_folderpath}/database'
kg_folderpath = f'{database_folderpath}/kg'

def entities_normalization():
    triples_raw_folderpath = f'{kg_folderpath}/0003-abstracts-triples-raw'
    triples_raw_filenames = sorted(os.listdir(triples_raw_folderpath))
    for triples_raw_filename_i, triples_raw_filename in enumerate(triples_raw_filenames):
        print(f'{triples_raw_filename_i}/{len(triples_raw_filenames)}')
        triples_raw_filepath = f'{triples_raw_folderpath}/{triples_raw_filename}'
        with open(triples_raw_filepath) as f: content = f.read()
        # print(content)
        print()
        print()
        print()
        triples = []
        for line in content.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('[') and line.endswith(']'):
                line = line[1:]
                line = line[:-1]
                triple = [item.strip() for item in line.split(',')]
                if len(triple) == 5:
                    triples.append(triple)
        running = True
        while running:
            en_filepath = f'{kg_folderpath}/knowledge_graph_entity_normalization.txt'
            with open(en_filepath) as f: en_content = f.read()
            en_lines = en_content.split('\n')
            entities_normalized = []
            for en_line in en_lines:
                en_line = en_line.strip()
                if en_line == '': continue
                en_line = en_line.replace('[', '')
                en_line = en_line.replace(']', '')
                en_chunks = [chunk.strip() for chunk in en_line.split('|')]
                entity_names = [item.strip() for item in en_chunks[0].split(',')]
                entity_types = [item.strip() for item in en_chunks[1].split(',')]
                # print(entity_names)
                # print(entity_types)
                entities_normalized.append([entity_names, entity_types])
            # print(entities_normalized)
            for triple in triples:
                entity_1 = triple[0].strip()
                entity_type_1 = triple[1].strip()
                entity_2 = triple[3].strip()
                entity_type_2 = triple[4].strip()
                # print(f'{entity_1} ({entity_type_1})')
                # print(f'{entity_2} ({entity_type_2})')
                # print(triple)
                triple_normalized = [x for x in triple]
                for entity_normalized in entities_normalized:
                    if (
                        entity_1.lower().strip() in [e.lower() for e in entity_normalized[0]] and
                        entity_type_1.lower().strip() in [e.lower() for e in entity_normalized[1]]
                    ):
                        triple_normalized[0] = entity_normalized[0][0]
                        triple_normalized[1] = '__' + entity_normalized[1][0] + '__'
                    if (
                        entity_2.lower().strip() in [e.lower() for e in entity_normalized[0]] and
                        entity_type_2.lower().strip() in [e.lower() for e in entity_normalized[1]]
                    ):
                        triple_normalized[3] = entity_normalized[0][0]
                        triple_normalized[4] = '__' + entity_normalized[1][0] + '__'
                print(triple_normalized)
            cmd = input('>>')
            if cmd == '': continue
            else: running = False
        # quit()
        # print(triples_raw_filepath)

def industries_files_parse():
    input_folderpath = f'{kg_folderpath}/0004-industries'
    input_filenames = sorted(os.listdir(input_folderpath))
    industries_names = []
    for input_filename_i, input_filename in enumerate(input_filenames):
        print(f'{input_filename_i}/{len(input_filenames)}')
        input_filepath = f'{input_folderpath}/{input_filename}'
        # with open(input_filepath) as f: content = f.read()
        input_data = io.json_read(input_filepath)
        # with open(input_filepath) as f: content = f.read()
        extracted_text = input_data['extracted_text']
        lines = []
        for line in extracted_text.split('\n'):
            line = line.strip()
            if line == '': continue
            if line.startswith('`'): continue
            lines.append(line)
        extracted_text_cleaned = '\n'.join(lines)
        try: extracted_data = json.loads(extracted_text_cleaned)
        except:
            print(extracted_text_cleaned)
            # quit()
        if extracted_data == {}: continue
        try: triples = extracted_data['triples']
        except:
            print(extracted_data)
            quit()
        for triple in triples:
            industry_name = triple['entity2_name']
            industries_names.append(industry_name)
        if input_filename_i > 100000:
            break
    industries_names = sorted(list(set(industries_names)))
    for industry_name in industries_names:
        print(industry_name)
    industries_names = '\n'.join(industries_names)
    output_folderpath = f'{kg_folderpath}/0005-industries-names'
    output_filepath = f'{output_folderpath}/industries-names.txt'
    io.file_write(output_filepath, industries_names)

# industries_files_parse()

import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
# G = nx.DiGraph()
# G = nx.MultiGraph()
# G = nx.MultiDiGraph()

'''
G.add_node('Herbal Medicine')

G.add_node('Herbs')
G.add_node('Phytochemicals')
G.add_node('Conditions')
G.add_node('Preparations')

G.add_node('Infusions')
G.add_node('Decoctions')
G.add_node('Tinctures')
'''

triplets = [
    ('herbal tradtitions', 'favor', 'infusion'),
    ('herbal tradtitions', 'favor', 'decoction'),
    ('infusion', 'uses', 'medicinal plants'),
    ('decoction', 'uses', 'medicinal plants'),
    ('infusion', 'is a form of ', 'extraction'),
    ('decoction', 'is a form of ', 'extraction'),
    ('infusion', 'is a', 'liquid preparation'),
    ('infusion', 'is a', 'extraction method'),
    ('infusion', 'is derived from', 'Latin "infundere"'),
    ('infusion', 'contains', 'nutritional principles'),
    ('infusion', 'contains', 'medicinal principles'),
    ('infusion', 'contains', 'inert or passive constituents'),
    ('infusion', 'contains', 'tonic minerals'),
    ('infusion', 'contains', 'pro-biotic fodder'),
    ('infusion', 'can contain', 'starch (via hot water)'),
    ('infusion', 'can contain', 'albumin (via cold water)'),
    ('infusion', 'can contain', 'gum, sugar, and other extractives'),
    ('infusion', 'uses', 'water (mestruum)'),
    ('infusion', 'uses', 'vinegar (mestruum)'),
    ('infusion', 'uses', 'dilute glycerin (mestruum)'),
    ('infusion', 'uses', 'wine (mestruum)'),
    ('infusion', 'uses', 'juice (mestruum)'),
    ('infusion', 'can be made via', 'maceration'),
    ('infusion', 'can be made via', 'digestion'),
    ('infusion', 'can be made via', 'percolation'),
    ('infusion', 'requires', 'closed vessels'),
    ('infusion', 'requires', 'suitable vessels'),
    ('infusion', 'requires', 'immediate use'),
    ('infusion', 'best prepared in', 'glazed earthenware'),
    ('infusion', 'best prepared in', 'porcelain'),
    ('infusion', 'best prepared in', 'glass'),
    ('infusion', 'should avoid', 'tinned iron'),
    ('infusion', 'should avoid', 'aluminum'),
    ('infusion', 'should avoid', 'metallic vessels'),
    ('infusion', 'is prepared by', 'hot water'),
    ('infusion', 'is prepared by', 'cold water'),
    ('infusion', 'is prepared by', 'boiling water'),
    ('infusion', 'can be prepared as', 'hot infusion'),
    ('infusion', 'can be prepared as', 'cold infusion'),
    ('infusion', 'is suitable for', 'flowers'),
    ('infusion', 'is suitable for', 'most leaves'),
    ('infusion', 'is suitable for', 'soft stems'),
    ('infusion', 'is suitable for', 'soft tissue plants'),
    ('infusion', 'is suitable for', 'some roots'),
    ('infusion', 'is suitable for', 'chamomile'),
    ('infusion', 'is suitable for', 'peppermint'),
    ('infusion', 'is suitable for', 'valerian root'),
    ('infusion', 'is suitable for', 'red clover blossoms'),
    ('infusion', 'is suitable for', 'slippery elm bark (cold infusion'),
    ('infusion', 'is suitable for', 'marshmallow root (cold infusion'),
    ('infusion', 'provides', 'hydration'),
    ('infusion', 'provides', 'pro-biotic proliferation'),
    ('infusion', 'serves as', 'tonic beverage'),
    ('infusion', 'serves as', 'plant medicine'),
    ('infusion', 'serves as', 'herbal food'),
    ('infusion', 'has limited', 'shelf-life/preservation'),
    ('infusion', 'recommended dosage', 'one cupful three times a day (standard)'),

    ('tinctures', 'type of', 'fractional extracts'),
    ('tinctures', 'have high', 'concentation'),
    ('fractional extracts', 'have high', 'concentation'),
    ('last 100 years', 'characterized by', 'emphasis on concentrated extracts'),

    ('alcohol', 'serves as', 'solvent'),
    ('glycerin', 'serves as', 'solvent'),
    ('alcohol', 'is used for', 'tinctures'),
    ('glycerin', 'is used for', 'tinctures'),
]

triples = [
    ('ozone', 'instance_of', 'simple substance'),
    ('ozone', 'instance_of', 'allotrope of oxygen'),
    ('ozone', 'instance_of', 'type of chemical entity'),
    ('ozone', 'subclass_of', 'oxidizing agent'),
    ('ozone', 'has_use', 'sterilization'),
    ('ozone', 'associted_hazard', 'ozone exposure'),
    ('ozone', 'chemical_formula', 'O3'),
    ('ozone', 'subject_has_role', 'photochemical oxidant'),
    ('ozone', 'has_part(s)', 'oxygen'),
    ('ozone generator', 'instance_of', 'electrical appliance'),
]

triples = [
    ["Ozone treatment", "technology", "is", "food-processing technology", "technology"],
    ["Ozone treatment", "technology", "has attribute", "cost-effective", "property"],
    ["Ozone treatment", "technology", "has attribute", "eco-friendly", "property"],
    ["Ozone treatment", "technology", "used for removal of", "milk residues", "substance"],
    ["Ozone treatment", "technology", "used for removal of", "biofilm-forming bacteria", "organism"],
    ["milk residues", "substance", "found on", "stainless steel surfaces", "material"],
    ["biofilm-forming bacteria", "organism", "found on", "stainless steel surfaces", "material"],
    ["Ozone treatment", "technology", "used in", "milk processing", "process"],
    ["milk processing", "process", "includes", "fluid milk", "product"],
    ["milk processing", "process", "includes", "powdered milk products", "product"],
    ["milk processing", "process", "includes", "cheese", "product"],
    ["Ozonation", "process", "prevents", "mould growth", "biological process"],
    ["mould growth", "biological process", "occurs on", "cheese", "product"],
    ["Ozonation", "process", "inactivates", "airborne moulds", "organism"],
    ["airborne moulds", "organism", "present in", "cheese ripening facilities", "facility"],
    ["airborne moulds", "organism", "present in", "storage facilities", "facility"],
    ["Ozone treatment", "technology", "reduces", "pollutants", "substance"],
    ["pollutants", "substance", "found in", "dairy wastewaters", "waste"],
]

triples = [
    ['mould growth', 'problem', 'where', 'cheese', 'location'],
    ['airborne moulds', 'problem', 'where', 'cheese ripening and storage facilities', 'location'],
    ['pollutants', 'problem', 'where', 'dairy wastewaters', 'location'],
    ['milk residues', 'problem', 'where', 'stainless steel surfaces', 'location'],
    ['biofilm-forming bacteria', 'problem', 'where', 'stainless steel surfaces', 'location'],
]

triples = [
    ["milk residues", "problem", "present_in", "stainless steel surfaces", "location"],
    ["milk residues", "problem", "present_in", "milk processing", "location"],
    ["milk residues", "problem", "present_in", "fluid milk", "location"],
    ["milk residues", "problem", "present_in", "powdered milk products", "location"],
    ["milk residues", "problem", "present_in", "cheese", "location"],
    ["biofilm-forming bacteria", "problem", "present_in", "stainless steel surfaces", "location"],
    ["biofilm-forming bacteria", "problem", "present_in", "milk processing", "location"],
    ["biofilm-forming bacteria", "problem", "present_in", "fluid milk", "location"],
    ["biofilm-forming bacteria", "problem", "present_in", "powdered milk products", "location"],
    ["biofilm-forming bacteria", "problem", "present_in", "cheese", "location"],
    ["mould growth", "problem", "present_in", "cheese", "location"],
    ["mould growth", "problem", "present_in", "cheese ripening and storage facilities", "location"],
    ["airborne moulds", "problem", "present_in", "cheese ripening and storage facilities", "location"],
    ["pollutants in dairy wastewaters", "problem", "present_in", "dairy wastewaters", "location"]
]
triples = [[row[0], row[2], row[3]] for row in triples]

triples = []
for line in io.file_read('C:/vault/ozonogroup/database/kg/relationships/all.txt').split('\n'):
    line = line.strip()
    if line == '': continue
    line = line.split(',')
    triples.append(line)
triples = [[row[0], row[2], row[3]] for row in triples]

for s, p, o in triples:
    G.add_edge(s, o, predicate=p)

pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue')

edge_labels = nx.get_edge_attributes(G, 'predicate')

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()

