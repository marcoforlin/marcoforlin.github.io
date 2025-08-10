import csv
import json

daos_links = dict()
with open('daos_links.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        daos_links[row[0]] = row[1]

# Load the first JSON file
with open('merged_impactdaos.json', 'r') as f1:
    data1 = json.load(f1)

    for d in data1['nodes']:
        if d['name'] in daos_links:
            d['link'] = daos_links[d['name']]

    # Write the merged data to a new file
    with open('merged_impactdaos_wlinks.json', 'w') as outfile:
        json.dump(data1, outfile, indent=2)
    
