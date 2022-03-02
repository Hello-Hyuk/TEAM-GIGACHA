import rospy
from planner_and_control.msg import Path
import csv
from numpy import rad2deg

def read_global_path(name):
        global_path = Path()
        with open("/home/inha/TEAM-GIGACHA/src/planner_and_control/script/lib/mapping_utils/maps/aerospace_campus_fin/" + name + ".csv", mode="r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for line in csv_reader:
                global_path.x.append(float(line[0]))
                global_path.y.append(float(line[1]))
                #global_path.k.append(float(line[2]))
        return global_path
