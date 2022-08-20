import json


files=['global_path_1.json','global_path_2.json','global_path_3.json','global_path_4.json']

def merge_JsonFiles(filename):
    data_dict = dict()
    data_list = []
    for f1 in filename:
        with open(f1, 'r') as infile:
            data = json.load(infile)
            data_list.extend(data.values())

    for n, nodes in enumerate(data_list):
        data_dict[n] = nodes
    
    j = json.dumps(data_dict, indent = 4)
    f = open('map.json', 'w')
    print(j, file = f)
    f.close()

merge_JsonFiles(files)