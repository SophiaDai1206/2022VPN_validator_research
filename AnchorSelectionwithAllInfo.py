import csv

#use beautiful soup to extract the data of all time coonnection
import requests
import re
from bs4 import BeautifulSoup
def get_data():
    with open('anchorSelection.csv','r') as csvinput:
        with open('anchorSelectionAll.csv', 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            reader = csv.reader(csvinput)

            all = []
            header = next(reader)
            n=1
            #for every row in anchorSelection.csv this program will run
            for row in reader:
                # url changes according to the id of the anchor and beautiful soap gets the data from the page
                URL = "https://atlas.ripe.net/frames/probes/" + row[2] + "/"
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")

                # extract the All Time connection percentage
                table = soup.find('table', {"class": "resolutions table table-condensed"})
                list = table.find_all(text=re.compile("%"))
                # search if there is "Still Connected" in the frame code
                sign = soup.find_all(text=re.compile("Still Connected"))
                if sign == []:
                    row.append("Not Connected")
                else:
                    row.append("Connected")

                # extract the ping info
                table_1 = soup.find("table", {"class": "table table-condensed table-striped table-hover"})
                Anchor_ping = table_1.find(text=re.compile("anchors"))

                if str(Anchor_ping) == "None":
                    print("Empty", Anchor_ping)
                    Anchor_ping = []
                else:
                    Anchor_ping = Anchor_ping.replace('(', '').replace(')', '').replace("anchors", "")

                table_2 = soup.find_all("table", {"class": "table table-condensed table-striped table-hover"})[1]
                Probes_ping = table_2.find_all(text=re.compile("probes"))


                if len(Probes_ping) == 0:
                    print("Empty", Probes_ping)
                    Probes_ping = []
                else:
                    Probes_ping = Probes_ping[0].replace('(', '').replace(')', '').replace("probes", "")

                # label the progress
                row.append(list[-1])
                row.append(Anchor_ping)
                row.append(Probes_ping)
                all.append(row)
                print(n, row)
                n = n + 1

            writer.writerow(header + ["All Time"] + ["Status"]+["anchors p"] + ["probes p"])
            writer.writerows(all)




if __name__ == '__main__':
  get_data()