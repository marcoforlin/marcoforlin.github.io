import json


def clearId(id):
    id = id.lower()
    if id[:3] == "the":
        id = id[3:]
    if 'greenpill' in id:
        return 'greenpill'
    if 'impactdaos' in id:
        return id
    
    return id.replace(" ", "-").replace("_", "").replace("-", "").replace("dao", "").replace('\u00f2', 'o').replace('\u00f3', 'o')

# Load the first JSON file
with open('impactdaos2.json', 'r') as f1:
    data1 = json.load(f1)

# Load the second JSON file
with open('impactdaos.json', 'r') as f2:
    data2 = json.load(f2)

# Get the list of DAOs from both files
daos1 = data1.get('daos', [])
daos2 = data2.get('daos', [])
links1 = data1.get('links', [])
links2 = data2.get('links', [])
toremove = []

# find duplicates
for d1 in daos1:
    for d2 in daos2:
        d1tmp = clearId(d1['id'])
        d2tmp = clearId(d2['id'])
        if d1tmp == d2tmp:
            print(f"Duplicate DAO: {d1}")
            toremove.append(d2)
            d1['id'] = clearId(d1['id'])    
        else:
            d1['id'] = clearId(d1['id'])
            d2['id'] = clearId(d2['id'])

# Merge the lists of DAOs
merged_daos = daos1
for d in daos2:
    if d not in toremove:
        merged_daos.append(d)

links = links1 + links2      
for l in links:
    l['source'] = clearId(l['source'])



# Create the new data structure
merged_data = {
    'nodes': sorted(merged_daos, key=lambda x: x['id']),
    'links': links
}

# Write the merged data to a new file
with open('merged_impactdaos.json', 'w') as outfile:
    json.dump(merged_data, outfile, indent=2)

print(f"Successfully merged {len(merged_daos)} DAOs into merged_impactdaos.json")


