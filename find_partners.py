from langchain_huggingface import HuggingFaceEndpoint
from langchain import HuggingFaceHub
from langchain_community.tools import BraveSearch
from langchain_tavily import TavilySearch
from getpass import getpass
import json
import os
import time

#assumption is that we already gathered all the DAOs in the merged_impactdaos_wlinks.json file
#taking them from ImpactDaos.xys and the 2 Greenpill books.
#This was done non-programmatically using NotebookLM to generate json, then merged them using merge.py.
#I also used perplexity to find all the links. => all of this could be automated using langchain as well
#We now want to find the partners of each DAO, using tavily to crawl the web.
#then we want to add the partners to the merged_impactdaos_wlinks.json file.

## WATCH IT: this may go on forever recursively, I decided to stop it manually once it reached far enough from the original
## DAOs landscape

# --- Load environment variables from .env file ---
load_dotenv()

from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# Load the first JSON file
with open('all_daos.json', 'r') as f1:
    data1 = json.load(f1)

for d in data1['nodes']:

    print("finding partners for: " + d['link'])
    
    if 'partners' not in d:
        d['partners'] = []
        try:
            response = tavily_client.crawl(d['link'], instructions="Find pages containing ecosystem partners")
            for r in response['results']:
                base_url = r['url'].split("/")[2]
                
                if d['link'] not in base_url and d['id'] not in base_url and d['name'].lower() not in base_url and base_url not in d['partners']:
                    # print(r['url'])
                    d['partners'].append(base_url)

                    #if the url is not in the list, add it
                    node = list(filter(lambda x: x['id'].lower() in base_url or x['name'].lower() in base_url, data1['nodes']))
                    if len(node) == 0:
                        print("adding new node: " + base_url)
                        node = {'id': base_url, 'name': base_url, 'category': 'Unknown', 'type': 'Unknown', 'description': 'Unknown', 'link': base_url} 
                        data1['nodes'].append(node)
                    else:
                        node = node[0]
                        print("node already exists: " + base_url)
                    #add a link between the two organizations
                    data1['links'].append({'source': d['id'], 'target': node['id']})

            #update partners
            data1['nodes'][data1['nodes'].index(d)]['partners'] = d['partners']
            time.sleep(1)
            # print(response)
        except Exception as e:
            print(e)

# Write the merged data to a new file
with open('all_daos.json', 'w') as outfile:
    json.dump(data1, outfile, indent=2)


