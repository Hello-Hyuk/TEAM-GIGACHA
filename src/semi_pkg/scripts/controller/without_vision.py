'''
비전 정보 받기 전 모라이에서 돌려볼 코드

2022/12/17 02:00 :: 클래스 구조에서 일반 함수로 변경
                    인지팀한테 장애물이 객체 하나로 유지될 수 있는지 확인해봐야함

<구상>
1. 가정
 - 차량의 ENU좌표를 알고 있음
 - 장애물의 ENU좌표를 알고 있음
 - steer하는 데 걸리는 시간은 매우 적음
 - att_heading과 potential field의 좌표축은 일치함

2. 목표
 - 장애물에 대한 척력장 만들기
 - Total force를 speed와 steer로 변환하기

3. 세부 목표
 - 장애물에 대한 척력장 만들기
  1) 장애물이 점멸할 때는 어떻게?
     ex) bbox가 아주 빠르게 잡혔다 안 잡혔다를 반복

 - Total force를 speed와 steer로 변환하기
  1) 현재 speed와 att_heading으로부터 차량에 가해진 힘(original force)을 계산
  2) Original force와 척력을 더하여 다시 speed와 steer로 변환

'''


import numpy as np
from math import atan2, cos, sin
from .intersection import intersection

def get_f_rep(ego, P_obs, V_obs, n2_w):
    # 기본 파라미터 설정
    P_veh = [ego.x, ego.y] # 차량 위치
    V_veh = [ego.speed*cos(ego.heading),ego.speed*sin(ego.heading)] # 차량 속도
    R_s = 0 # 이거보다 작은면 충돌로 가정
    R_0 = 10000 # 물체가 영향을 미치는 거리
    a_max = 5 # 가속도 최대치
    P_vehobs = np.linalg.norm(np.subtract(P_obs, P_veh)) # 장애물과 차량의 상대거리
    V_vehobs = np.linalg.norm(np.subtract(V_obs, V_veh)) # 장애물과 차량의 상대속도

    # 상대거리 업데이트
    last_P_obsveh_updated = P_vehobs

    # 척력장(F_rep1) 가중치
    w_rep = 200

    
    ## 식 (5) 구현부 (F_rep1)
    size = -(w_rep/(P_vehobs - R_s)**2)*(1 + V_vehobs/a_max)
    n_RO = np.subtract(P_veh, P_obs)/P_vehobs
    F_rep1 = n_RO * size

    ## 식 (6) 구현부(F_rep2)
    size = (n2_w * V_vehobs) / (P_vehobs * a_max * (P_vehobs - R_s)**2)


    # 물체가 차량 기준 왼쪽인지 오른쪽인지
    # 외적을 위해 z값에 0 추가
    # V_veh_for_cross = [V_veh[0], V_veh[1], 0]
    # P_obsveh_for_cross = [np.subtract(P_veh, P_obs)[0], np.subtract(P_veh, P_obs)[1], 0]

    # 물체 방향 결정
    if V_veh[1]*np.subtract(P_veh, P_obs)[0]-V_veh[0]*np.subtract(P_veh, P_obs)[1] > 0:
        obs_dir = "right"
    else:
        obs_dir = "left"
    print(obs_dir)

    # atan2 nan 방지
    V_veh_size = np.linalg.norm(V_veh) + 1e-6

    # F_rep2 방향 결정, 멀어질 때 척력 제거
    # if 90<intersection(V_veh, n_RO) and P_vehobs-R_s>0 and P_vehobs-R_s<R_0:
    print()
    if 90<intersection(V_veh, n_RO):
        if obs_dir == "left":
            n2 = [V_veh[1]/V_veh_size, -V_veh[0]/V_veh_size]
        elif obs_dir == "right":
            n2 = [-V_veh[1]/V_veh_size, V_veh[0]/V_veh_size]
        
        F_rep2 = np.multiply(n2, size)
    else:
        F_rep1 = 0
        F_rep2 = 0

    return F_rep1+F_rep2, last_P_obsveh_updated

   

def get_n2_w(ego, P_obs, att_heading):
    sight = 80
    max = 12
    min = 3

    P_veh = [ego.x, ego.y]
    a = [cos(np.radians(att_heading)), sin(np.radians(att_heading))]
    b = np.subtract(P_veh, P_obs) 
    alpha = atan2(a[1], a[0])
    beta = atan2(b[1], b[0])
    theta = np.degrees(beta - alpha)

    if theta > (180-sight/2) and theta < 180:
        w_rep = ((max-min)/(sight/2))*(theta-180) + max
    elif theta < (180+sight/2) and theta >= 180:
        w_rep = -((max-min)/(sight/2))*(theta-180) + max
    else:
        w_rep = min
        
    return w_rep
    # return 1



def ss2f(speed, att_heading, force_potential_field):
    a = [cos(np.radians(att_heading))*speed, sin(np.radians(att_heading))*speed]
    b = force_potential_field
    c = np.add(a, b)
    alpha = atan2(a[1], a[0])
    gamma = atan2(c[1], c[0])
    theta = np.degrees(gamma - alpha)
    if theta>180:
        theta-=360

    return theta