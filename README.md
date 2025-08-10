## GOAL
Build a database of all the DAOs in the ReFi space, and their links.

# Data acquisition
1. The DAO data was acquired form ImpactDaos.xyz and the latest Greenpill book.

# Data processing
2. Used NotebookLM to generate a list of all the DAOs and classifications from all sources.
3. Merged them using merge.py. Some heuristics involved to account for the fact that some DAOs were mentioned in multiple sources.
4. Used perplexity to find all the links.
Prompt: "search online all the links for all the name fields in the nodes list. don't output json, just output a csv with name, link" 
5. Run links.py to merge the web-links into the json file.
6. Asked Gemini to identify the classifications of each DAO.
Prompt: "given the list of nodes in the json file, classify them based on the description as one of these categories: Decentralized Science (DeSci), Community Funding Protocols, Regenerative Finance (ReFi),Climate and Environmental REGENeration,Culture,Education,Infrastructure,Impact Measurement,Applied Research,Regenerative Economy. Commons Pools. If a node already has category matching one of the above, don't reclassify it. store the output in a new updated json."
7. Run main.py to find the partners of each DAO. 
This uses tavily to crawl the website of each node and find the partners. Note that this is not perfect and some partners might be missed.
This does a recursive search, looking for partners, and then partners of partners, and for now it was stopped manually after it started getting too far.
This imples that the graph includes organization pretty far from the original ImpactDAO subset, and some of them are not even ReFi related, notably Chevron and other big corporations.

8. Run update_nodes.py : For all the newly added partners, grab the website content and use Qwen to write a description and classify them. Classification is done according to the same categories as in step 6, with the addition of Venture Capital and Other, to avoid gross misclassifications. 
Note that for the LLM, difference between carbon credits and regenerative economic isn't obvious, so some cleanup will be needed.

## Data visualization
9. Serve index.html to visualize the graph.

## NOTES
This whole thing was done step by step as I saw the data that were coming in, and required some manual editing to clean up the data and fix some issues. 
