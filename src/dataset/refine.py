#!/usr/bin/env python3
import os

dir_path = '/home/jay/DataSets/bdd100k/images/100k/val'
class0 = int()
class1 = int()
class2 = int()
class3 = int()
class4 = int()
class5 = int()
class11 = int()
cnt = int()

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.txt' in file:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                lines = f.readlines()                    
                print(lines)
                
            with open(file_path, "w") as f: 
                for line in lines:
                    class_num = line.split()[0] 
                    print("before : ",line)
                    tmp = line.split()
                    if class_num == '0':
                        tmp[0] = '0'
                        class0 += 1 
                    elif class_num == '2':
                        tmp[0] = '2'
                        class1 += 1
                    elif class_num == '3':
                        tmp[0] = '5'
                        class2 += 1
                    elif class_num == '4':
                        tmp[0] = '4'
                        class3 += 1 
                    elif class_num == '6':
                        tmp[0] = '3'
                        class4 += 1
                    elif class_num == '7':
                        tmp[0] = '1'
                        class5 += 1
                    # if class_num == '10':
                    #     tmp[0] = '5'
                    #     class11 += 1    
                    if class_num == '0' or class_num == '2' or class_num == '3' or class_num == '4' or class_num == '6' or class_num == '7':
                        f.write(' '.join(tmp)+'\n')
                print(file_path," : refine ends")
                   

print("person : ", class0)
print("bicycle : ", class1)
print("car : ", class2)
print("motocycle : ", class3)
print("bus : ", class4)
print("truck : ", class5)