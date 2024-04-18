import requests
import json
from ufc import *


# url = "https://api.sportsdata.io/v3/mma/scores/json/Schedule/UFC/2024?key=54ff2408426443e3965ebbacd18ce624"
# response = requests.get(url)
# json_res = response.json()
# print(json.dumps(json_res, indent=4))

jsonResponse = get_fighter("Arman Tsarukyan")
print(json.dumps(jsonResponse, indent=4))

jsonResponse = get_ufc_stats("https://www.sherdog.com/events/UFC-300-Pereira-vs-Hill-100836")
print(json.dumps(jsonResponse, indent=4))