#export PATH=$PATH:/home/byron/workspace/campgroundreviews/geckodriver-v0.26.0-linux64

import requests
import csv
import json
import time
from selenium import webdriver
from random import randint

driver = webdriver.Firefox()

url_base = "https://api.campgroundreviews.com"
headers = {'accept':'application/x.rvparkreviews.v3+json'}
# park_search = '/photos-for-park/'
recent_reviews = '/recent-reviews?page=1&sort=true&withAll=true&ratedSort=null&rvSort=null&limit=1&park='
# count_park = 0
count_recent_reviews = 0
counnt_driver = 0


with open('states.json') as file_states:
    states = json.load(file_states)

for state in states['states']:
    print("\t\t\t---------------------> Starting "+state['name'])
    i = 0
    file_csv = open('final_'+state['name']+'.csv','w')
    writer = csv.writer(file_csv)
    writer.writerow(["name","state","city","address","zip","lat","lon","elevation","phone","website","sites","CovidStatus","pullthru","rating","average rate"])
    with open('data_states/'+state['name']+'.json') as parks:
        parks = json.load(parks)
        total_state = str(len(parks))
        for park in parks:
            i+=1
            data = []
            print('starting '+park['name']+' id: '+str(park['id'])+' '+str(i)+"/"+total_state)
            print("making reviews")
            time.sleep(randint(12,20))
            r = requests.get(url=url_base+recent_reviews+str(park['id']),headers=headers)
            if len(r.json()['data']) == 0:
                # print("making park")
                # r = requests.get(url=url_base+park_search+str(park['id']),headers=headers)
                # if len(r.json()['tags']) == 0:
                time.sleep(randint(12,20))
                counnt_driver += 1
                print("making driver")
                driver.get(park['url'])
                park = driver.execute_script('return parkResource')
                # else:
                #     count_park += 1
                #     time.sleep(15)
                #     info_park = r.json()
                #     park = info_park['tags'][0]['photos'][0]['park']
            else:
                count_recent_reviews += 1
                info_park = r.json()
                park = info_park['data'][0]['park']
            
            data.append(park['name'])
            data.append(park['region']['name'])
            data.append(park['city']['name'])
            data.append(park['address'])
            data.append(park['zip'])
            data.append(park['lat'])
            data.append(park['lon'])
            data.append(park['elevation'])
            data.append(park['phone'])
            data.append(park['website'])
            data.append(park['sites'])
            data.append(park['covidStatus'])
            data.append(park['cg_pullthru'])
            data.append(park['rating_avg'])
            data.append(park['avg_rate'])
            writer.writerow(data)
            print("reviews: {count_recent_reviews}| driver: {counnt_driver}".format(count_recent_reviews=str(count_recent_reviews),counnt_driver=str(counnt_driver)))
            print('complete '+park['name']+str(i)+"/"+total_state)
    file_csv.close()

