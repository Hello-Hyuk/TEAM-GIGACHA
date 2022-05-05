import csv

def combine_csv(number_of_files):
    
    real_array = []
    float_array = []

    for i in range(1, number_of_files+1):
        with open(f'maps/Siheung/maps/left/{i}.csv',\
             mode="r", newline = '') as csv_file:
            for line in csv_file.readlines():
                array = line.split(',')
                float_array = [float(array[0]), float(array[1])] #, float(array[2])]
                real_array.append(float_array)
            
    with open('maps/Siheung/maps/left/turn_left.csv',\
         'w', newline = '') as all_nodes_file: 
        writer = csv.writer(all_nodes_file)
        writer.writerows(real_array)

combine_csv(3)