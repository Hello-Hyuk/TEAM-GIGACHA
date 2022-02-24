#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymap3d as pm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from lib.cubic_spline_planner import calc_spline_course


# 기준점 (원점) 11번 (최종)노드로 fix 함.
# base_lat = 37.239238   
# base_lon = 126.773157
# base_alt = 30.3

# 송도
# base_lat = 37.383784   
# base_lon = 126.654310
# base_alt = 15.4
# 송도 건물 옆
# base_lat = 37.3851693 #새로운 베이스
# base_lon = 126.6562271
# base_alt = 15.4

#simul
base_lat = 37.239235 
base_lon = 126.77315833333333
base_alt = 15.4

def get_xy(lat, lon, alt): #점들 사이의 새로운 점들을 설정 
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)
    return e, n

def cubic(name, number,*args): # args에는 1,2,3,4,5,6 등 막 들어 수있음

    colnames=['lon', 'lat']
    df = pd.read_csv(f'nodes/{name}.csv', names=colnames, header=None)
    x=[]
    y=[]
    
    for i in args: # i=1,2,3,...
        latitude = df.loc[i-1,'lat'].tolist() # 
        longitude = df.loc[i-1,'lon'].tolist() # 0 행 부터라서 index 1씩 빼줌
        output = get_xy(latitude, longitude, 0.5)
        x.append(output[0])
        y.append(output[1])

    cx, cy, cyaw, ck, s = calc_spline_course(x, y, ds=0.1)
    save_data = list(zip(cx, cy, cyaw, ck, s))

    save_df = pd.DataFrame(save_data)
    save_df.to_csv('maps/%s.csv'%csv_name, index=False, header = False)
    print(f"Map saved to maps/{csv_name}.csv")
    plt.scatter(cx, cy)    
    plt.show()

    return(cx, cy, cyaw, ck, s)


cubic("Campus", "1st_straight", 1,2)
cubic("Campus", "1st_corner", 2,3,4,5,6)
cubic("Campus", "2nd_straight", 6,7)
cubic("Campus", "2-3_midle_lane", 7,8)
cubic("Campus", "3rd_straight", 8,9,10)
cubic("Campus", "2nd_corner", 10,11,12,13,14,15)
cubic("Campus", "4th_straight", 15,16)
cubic("Campus", "3rd_corner", 16,17,18,19,20,21)
cubic("Campus", "5th_straight", 21,22)

# cubic("real_previous", 1,2,3,4,5,6,7,8,9,10,11,12,13,14)
# cubic("real_next", 1, 2)
