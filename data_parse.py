import json
from urllib.request import urlopen
import ssl
import csv
f = ("measurement_id_traceroute.csv",'r')
file = csv.DictReader(f)
header = next(file)
for row in file:
    jsonname = "traceroute_%s.json" %row[0]
    ssl._create_default_https_context = ssl._create_unverified_context
    URL = 'https://atlas.ripe.net//api/v2/measurements/%s/results/?format=json' %row[1]
    data = json.loads(urlopen(URL).read())

    list = []

    for i in range(len(data)):
        if data[i]['result']!= None:
            list.append({data[i]['prb_id']: data[i]['result']})
            # list.append(dictionary)

        json_object = json.dumps(list, indent=5)
        with open(jsonname, "w") as outfile:
            outfile.write(json_object)



# print(len(data))
# anchors = set()
# rtt_set = set()
# for i in range(len(data)):
#     if data[i]['result'][1].get('rtt') != None:
#         prb_id = data[i]['prb_id']
#         rtt = data[i]['result'][1]['rtt']
#         anchors.add(data[i]['prb_id'])
#         rtt_set.add(rtt)
#         print(prb_id)
#         print(rtt)
#     else:
#         rtt = None

# for i in range(len(data)):
#     if data[i]['result'][1].get('hop') != None:
#         prb_id = data[i]['prb_id']
#         hop = data[i]['result']
#         # [1]['hop']
#         # anchors.add(data[i]['prb_id'])
#         # rtt_set.add(rtt)
#         # print(prb_id)
#         # print(hop)
#     else:
#         hop = None


# countires = {}
# with open("anchorSelection.csv", "r") as f:
#     reader = csv.reader(f)
#     for row in reader:
#         if row[2] == "pid":
#             continue
#         if row[2] in anchors:
#             continue
#         if row[6] is not countires:
#             countires[row[6]] = 0
#         countires[row[6]] += 1
# print(countires)






