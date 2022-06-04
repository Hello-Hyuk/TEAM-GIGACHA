#!/usr/bin/env python3
from asyncio import FastChildWatcher
import os
import shutil

#dir_path = '/home/jay/DataSets/refine/coco/train/'
dir_path = '/home/jay/DataSets/bdd100k/images/100k/train/'
#dir_path = '/home/jay/DataSets/udacity/export/train/'
#dir_path = '/home/jay/DataSets/data/train/'
dst_path = '/home/jay/DataSets/data/tmp/train/'
tmp_path = '/home/jay/DataSets/refine/bdd/train/'

class0 = int()
class1 = int()
class2 = int()
class3 = int()
class4 = int()
class5 = int()
unknown = int()

#val
# #bdd
# person :  3556
# bicycle :  632
# car :  10830
# motocycle :  271
# bus :  1305
# truck :  825

# 10  ######
# person :  2828
# bicycle :  516
# car :  6576
# motocycle :  191
# bus :  1019
# truck :  644

# #####8
# person :  2272
# bicycle :  407
# car :  4396
# motocycle :  152
# bus :  784
# truck :  496

# 5
# person :  1082
# bicycle :  233
# car :  1467
# motocycle :  77
# bus :  397
# truck :  242

# person :  2850              4771
# bicycle :  700              1009
# car :  17633                18100
# motocycle :  327            698
# bus :  1601                 1864
# truck :  975                1090

#########################33

# person :  1921
# bicycle :  309
# car :  585
# motocycle :  371
# bus :  264
# truck :  115

# #coco
# person :  1395
# bicycle :  316
# car :  341
# motocycle :  371
# bus :  61
# truck :  63

##########
# person :  827
# bicycle :  214
# car :  511
# motocycle :  216
# bus :  212
# truck :  93

##########################33

# person :  68
# bicycle :  0
# car :  229
# motocycle :  0
# bus :  0
# truck :  226

#udacity
# # 10 
# person :  835
# bicycle :  0
# car :  4712
# motocycle :  0
# bus :  0
# truck :  1375

#8 ###############3
# person :  774
# bicycle :  0
# car :  3699
# motocycle :  0
# bus :  0
# truck :  1183

# 5
# person :  544
# bicycle :  0
# car :  1736
# motocycle :  0
# bus :  0
# truck :  723

carc = int()
perc = int()

ca = 4000

breaker1 = False
breaker2 = False

th1 = 100
th2 = 100

print(dir_path)
print("thresh hold : ",th1, th2)
print("-----balancing-----")
for (root, directories, files) in os.walk(dir_path):
    for file in files:
        car_flag = False
        per_flag = False
        motor = False
        bi = False
        bus = False
        truck = False
        car = False
        person = False
        img_cnt = 0
        ct0 = 0
        ct1 = 0
        ct2 = 0
        ct3 = 0
        ct4 = 0
        ct5 = 0
        ec = 0
        if '.txt' in file:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                lines = f.readlines()
                for line in lines:          
                    class_num = line.split()[0]
                    #print("before : ", line)
                    tmp = line.split()
                    if class_num == '0':
                       #tmp[0] = '2'
                       person = True
                       ct0 += 1
                    elif class_num == '1':
                       #tmp[0] = '0'
                       bus = True
                       ct1 += 1
                    elif class_num == '2':
                       car = True
                       #tmp[0] = '5'
                       ct2 += 1
                    elif class_num == '3':
                       #tmp[0] = '5'
                        motor = True
                        ct3 += 1
                    elif class_num == '4':
                        #tmp[0] = '5'
                        bi = True
                        ct4 += 1
                    elif class_num == '5':
                        #tmp[0] = '5'
                        truck = True
                        ct5 += 1
                    else:
                        ec += 1
                # if ct0 >= th1 or ct2 >= th2 :
                #     #or ct0 >= 1 or ct5 >= 2 10 2
                #     car_flag = True

                
                # if truck == True:
                #     if (ct5 >= 1) and ct2 <= 2 and ct0 <= 3:
                # if car == False :
                #     if (motor == True or bi == True or bus == True):
                        
                #     #if (ct1 >= 1 or ct3 >= 1 or ct4 >= 1) and ct2 <= 8: 
                    #if (ct1 >= 1 or ct3 >= 1 or ct4 >= 1) and ct0 < 10: 
                if truck == True:
                    if ct0 <= 0 and ct2 <=0 and ct1 <= 0 and ct3 <= 0 and ct4 <= 0 :
                        class0 += ct0
                        class1 += ct1
                        class2 += ct2
                        class3 += ct3
                        class4 += ct4
                        class5 += ct5
                        tmp_name = file.replace(".txt", "")
                        img = (dir_path+tmp_name).split('/')[-1] + '.jpg'
                        txt = (dir_path+tmp_name).split('/')[-1] + '.txt'
                        #print(img)
                        #shutil.move(dir_path + img, dst_path + img)
                        #shutil.move(dir_path + txt, dst_path + txt)
                        img_cnt += 1
                        if(img_cnt==8000):
                            breaker1=True
                else:
                    carc += 1
                    # shutil.move(dir_path + img, tmp_path + img)
                    # shutil.move(dir_path + txt, tmp_path + txt)
        if breaker1 == True :
            print("heart breaker")
            breaker2 = True
            break
    if breaker2 == True :
        print("almost done")
        break
    
print("person : ", class0)
print("bicycle : ", class1)
print("car : ", class2)
print("img number : ",img_cnt)
print("motocycle : ", class3)
print("bus : ", class4)
print("truck : ", class5)
print("else : ",carc)
print("else2 : ",unknown)