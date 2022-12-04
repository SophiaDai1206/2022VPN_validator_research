import csv

def anchor_selection_by_City():

    # Open the csv file
    with open('anchorSelectionAll.csv', newline='') as f:
        reader = csv.reader(f)
        data = [tuple(row) for row in reader]

    title = data[0]
    data.pop(0)

    anchor_list = []
    city_list = []

    final_data=[]

    # Make the names of city standard
    for i in range(len(data)):
        # a list with Anchor info
        anchor_list.append(data[i])
        city = name_standard(data[i][5])
        city_list.append(city)


    city_dictionary = {}
    for i in range(len(anchor_list)):
        if city_list[i] not in city_dictionary:
            city_dictionary[city_list[i]] = []
        city_dictionary[city_list[i]].append(anchor_list[i])


    # randomly choose one anchor per city
    for k, v in city_dictionary.items():
        # print(k)
        rand_index = random.randint(0, len(v)-1)
        final_data.append(v[rand_index])

    with open('AnchorSelection_city.csv', 'w', newline='') as csvfile:
        wr = csv.writer(csvfile, dialect="unix", quoting=csv.QUOTE_MINIMAL)
        wr.writerow(title)
        for lm in final_data:
            wr.writerow(lm)

def name_standard(name):
    if 'ü' in name:
        name.replace('ü', 'u')
    if 'é' in name:
        name.replace('é', 'e')
    if '-' in name:
        name.replace('-', ' ')
    if ' - ' in name:
        name.replace(' - ', ' ')

    name = name.split(',')[0]
    name.capitalize()
    return name

def anchor_selection_by_connectivity():
    with open('anchorSelectionAll.csv','r') as csvinput:
        with open('anchorselection_Connectivity.csv', 'w') as csvoutput:
            reader = csv.reader(csvinput)
            writer = csv.writer(csvoutput, lineterminator='\n')

            data = [tuple(row) for row in reader]
            title = data[0]
            data.pop(0)
            anchor_list_with_good_connectivity = []
            for i in range(len(data)):
                all_time = str(data[i][7])
                status = data[i][8].replace("%",'')
                status = float(status)
                # filter out low connected anchors: Not connected and status<92.44
                if all_time == "Connected":
                    if status >= 92.44:
                        anchor_list_with_good_connectivity.append(data[i])

            writer.writerow(title)
            for i in range(len(anchor_list_with_good_connectivity)):
                writer.writerows([anchor_list_with_good_connectivity[i]])




if __name__ == '__main__':
    # anchor_selection_by_City()
    # anchor_selection_by_connectivity()