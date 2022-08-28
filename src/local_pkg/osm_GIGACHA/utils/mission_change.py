import json

# ########################FINAL#########################
# stop_index_list = [1614, 2172, 3544, 4609, 5365, 5597, 5831, 6692, 8026, 8497]
# with open('/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/json_files/final_map.json') as json_file:
#     json_data = json.load(json_file)
# # 
#     list_1 = list(json_data.values())
# # 
#     for i in range(2491, 3415):
#         list_1[i][2] = "static_obstacle"
#     # 
#     for i in range(3776, 4402):
#         list_1[i][2] = "delivery"

#     for i in range(4402, 5153):
#         list_1[i][2] = "turn_left_traffic_light"
# # 
#     for i in range(5153, 5515):
#         list_1[i][2] = "U-TURN"

#     for i in range(5515, 5920):
#         list_1[i][2] = "non_traffic_right"
# # 
#     for i in range(5920, 6693):
#         list_1[i][2] = "delivery"
# # 
#     for i in range(6693, 9319):
#         list_1[i][2] = "driving"
# # 
#     for i in range(9319, 10300):
#         list_1[i][2] = "parking"
# 
#     # 
#     dict_1 = dict()
# # 
#     for n, (x, y , mission) in enumerate(list_1):
#         dict_1[n] = [float(x), float(y), mission]
# # 
#     j = json.dumps(dict_1, indent = 4)
#     f = open('final_map.json', 'w')
#     print(j, file = f)
#     f.close()
# 

stop_index_list = [1603, 2167, 3185]
with open('/home/gigacha/TEAM-GIGACHA/src/local_pkg/osm_GIGACHA/json_files/semi_final/semi_map.json') as json_file:
    json_data = json.load(json_file)

    list_1 = list(json_data.values())

    for i in range(711, 1023):
        list_1[i][2] = "parking"
    
    for i in range(1485, 1954):
        list_1[i][2] = "turn_left_traffic_light"

    for i in range(1954, 2506):
        list_1[i][2] = "static_obstacle"

    for i in range(2506, 3186):
        list_1[i][2] = "AEB"

    
    dict_1 = dict()

    for n, (x, y , mission) in enumerate(list_1):
        dict_1[n] = [float(x), float(y), mission]

    j = json.dumps(dict_1, indent = 4)
    f = open('semi_map.json', 'w')
    print(j, file = f)
    f.close()
    
    