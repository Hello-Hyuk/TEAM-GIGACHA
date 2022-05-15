#!/usr/bin/env python3
import os
import shutil

dir_path = '/home/jay/DataSets/data/train'

class0 = int()
class1 = int()
class2 = int()
class3 = int()
class4 = int()
class5 = int()
unknown = int()
cnt = int()

breaker1 = False
breaker2 = False

for (root, directories, files) in os.walk(dir_path):
    for file in files:
        if '.txt' in file:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                lines = f.readlines()                  
                for line in lines:
                    class_num = line.split()[0] 
                    #print("before : ",line)
                    tmp = line.split()
                    if class_num == '0':
                        #tmp[0] = '2'
                        class0 += 1 
                    elif class_num == '1':
                        #tmp[0] = '0'
                        class1 += 1
                    elif class_num == '2':
                        #tmp[0] = '5'
                        class2 += 1
                    elif class_num == '3':
                        #tmp[0] = '5'
                        class3 += 1
                    elif class_num == '4':
                        #tmp[0] = '5'
                        class4 += 1
                    elif class_num == '5':
                        #tmp[0] = '5'
                        class5 += 1
                    else:
                        unknown += 1

print("person : ", class0)
print("bicycle : ", class1)
print("car : ", class2)
print("motocycle : ", class3)
print("bus : ", class4)
print("truck : ", class5)
print("else : ",unknown)