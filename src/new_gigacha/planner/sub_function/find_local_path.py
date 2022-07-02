from math import sqrt

def findLocalPath(path, ego, cut_path):
    current_index = 0
    min_dis = float('inf')

    for i in range(len(path.x)):
        dx = ego.x - path.x[i]
        dy = ego.y - path.y[i]
        dis = sqrt(dx*dx + dy*dy)
        if dis < min_dis:
            min_dis = dis
            current_index = i
    
    if current_index + 100 > len(path.x):
        last_local_index = len(path.x)
    else:
        last_local_index = current_index + 100

    if len(cut_path.x) == 0:
        for i in range(current_index, last_local_index):
            cut_path.x.append(path.x[i])
            cut_path.y.append(path.y[i])
    else:
        count = 0
        for i in range(current_index, last_local_index):
            cut_path.x[count] = path.x[i]
            cut_path.y[count] = path.y[i]
            count += 1