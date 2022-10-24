import json
import csv

def csvTojson():
    with open('siStraight_.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data_dict = dict()
        list1 = []

        for row in csv_reader:
            list1.append(row)
            # print(list1)

        for n, (x, y) in enumerate(list1):
            data_dict[n] = [float(x), float(y)]
            data_dict[n].append("go")

    j = json.dumps(data_dict, indent = 4)
    f = open('siStraight.json', 'w')
    print(j, file = f)
    f.close()
            

csvTojson()