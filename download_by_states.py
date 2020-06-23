import requests
import json

url_base = "https://api.campgroundreviews.com"
headers = {'accept':'application/x.rvparkreviews.v3+json'}
parks_in_state = '/parks-in-state/'

with open('states.json') as file_states:
    states = json.load(file_states)
    file_states.close()

for state in states['states']:
    print("requesting "+state['name'])
    r = requests.get(url=url_base+parks_in_state+str(state['id']),headers=headers)
    with open('data_states/'+state['name']+'.json', 'w') as outfile:
        json.dump(r.json(), outfile)
    print('file '+state['name']+'.json saved')
