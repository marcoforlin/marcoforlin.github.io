import os
import json
import time
import tavily
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
load_dotenv()

from tavily import TavilyClient
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

with open('all_daos_updated.json', 'r') as f1:
    data1 = json.load(f1)

    for d in data1['nodes']:
        print("PROCESSING: "+ d['link'])

        if 'partners' not in d or not d['partners']:
            data1['nodes'][data1['nodes'].index(d)]['partners'] = []

        if d['description'] != "Unknown":
            print("already processed.")
        else:
            try:
                response = tavily_client.extract(d['link'])
            except Exception as e:
                print(f"Error during API call to tavily: {e}")
                time.sleep(1)
                continue

            if not response['results']:
                print("No results found for: "+ d['link'])
                time.sleep(1)
                continue
            if not response['results'][0]['raw_content']:
                print("No raw content found for: "+ d['link'])
                time.sleep(1)
                continue
            # print(response)

            # Get API keys from environment variables
            hyperbolic_api_key = os.getenv("HYPERBOLIC_API_KEY")

            if not hyperbolic_api_key:
                print("Error: Missing required API keys. Please set HYPERBOLIC_API_KEY in your .env file.")

            try:
                client = InferenceClient(
                    provider="hyperbolic",
                    api_key=hyperbolic_api_key
                )
            except Exception as e:
                print(f"Error initializing InferenceClient: {e}")

            messages = [
                {
                    "role": "user",
                    "content": "From the following html code, extract the description of the DAO, " \
                    "and categorize it based on the description as one of these categories: Venture Capital, Decentralized Science (DeSci), Community Funding Protocols, Regenerative Finance (ReFi),Climate and Environmental REGENeration,Culture,Education,Infrastructure,Impact Measurement,Applied Research,Regenerative Economy. Commons Pools. "\
                    "and if none fits, put Other."+ response['results'][0]['raw_content'] +"" \
                    "return description and category in this format: [description###category] without any additional text."
                }
            
            ]

            try:
                completion = client.chat.completions.create(
                    model="Qwen/Qwen2.5-72B-Instruct",
                    messages=messages
                )
            except Exception as e:
                print(f"Error during API call to summarization model: {e}")
                continue
            try:
                summary_text = completion.choices[0].message.content
                print("DESCRIPTION: "+summary_text.split("###")[0])
                print("CATEGORY: "+summary_text.split("###")[1])
                data1['nodes'][data1['nodes'].index(d)]['description'] = summary_text.split("###")[0]
                data1['nodes'][data1['nodes'].index(d)]['category'] = summary_text.split("###")[1]
                
            except Exception as e:
                print(f"Error parsing response: {e}")
                print(response['results'][0]['raw_content'])
                print(completion.choices[0].message.content)
                

            time.sleep(1)

            

with open('all_daos_updated.json', 'w') as outfile:
    json.dump(data1, outfile, indent=2)