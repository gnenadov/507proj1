
import requests

BASE_URL = "http://swapi.co/api/people" # only interested in people

resp = requests.get(BASE_URL)
results_object = resp.json()
people_list = results_object["results"]
print(people_list[0]) # print the first person in the list
exit()
