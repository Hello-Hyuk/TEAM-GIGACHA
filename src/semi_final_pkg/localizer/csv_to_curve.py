#!/usr/bin/env python3
import pandas as pd
import csv
import numpy as np
from math import atan2, sqrt

def csv_to_curve(name):
    with open('/home/gigacha/TEAM-GIGACHA/src/semi_final_pkg/maps/kcity_simul/left_lane.csv') as csv_file:
        csv_reader = pd.read_csv(csv_file, delimiter = ',', names = ['x', 'y', 'yaw', 'curvature', 'distance'])

        x_list = csv_reader['x'].values.tolist()
        y_list = csv_reader['y'].values.tolist()
        yaw_list = []
        curvature_list = []

        for i in range(len(x_list)-1):
            yaw = atan2(y_list[i] - y_list[i-1], x_list[i] - x_list[i-1])
            yaw_list.append((np.rad2deg(yaw)) % 360)

            if i == 0:
                x_vals = [x_list[-1], x_list[0], x_list[1]]
                y_vals = [y_list[-1], y_list[0], y_list[1]]
                R = circumradius(x_vals, y_vals)
                try:
                    curvature_list.append(1/R)
                except ZeroDivisionError:
                    curvature_list.append(0)
            else:
                R = circumradius(x_list[i-1:i+2], y_list[i-1:i+2])
                try:
                    curvature_list.append(1/R)
                except ZeroDivisionError:
                    curvature_list.append(0)
        
        save_data = list(zip(x_list, y_list, yaw_list, curvature_list))
        save_df = pd.DataFrame(save_data)
        save_df.to_csv('%s.csv' % name, index = False, header = False)

def circumradius(xvals, yvals):
    x1, x2, x3, y1, y2, y3 = xvals[0], xvals[1], xvals[2],\
    yvals[0], yvals[1], yvals[2]

    den = 2 * ((x2-x1) * (y3-y2)-(y2-y1) * (x3-x2))
    num = ( (((x2-x1)**2) + ((y2-y1)**2)) * (((x3-x2)**2) + ((y3-y2)**2)) * (((x1-x3)**2) + ((y1-y3)**2)) )**0.5

    if den == 0:
        return 0
    
    r = abs(num/den)

    return r

        
csv_to_curve('left_lane')
