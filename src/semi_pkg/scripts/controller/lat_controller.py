from math import hypot, cos, sin, atan2, degrees, atan2, radians, pi, sqrt
import numpy as np
from .without_vision import *



class LatController():
#    def __init__(self, eg, sh, lattice, pl, park, x=0.0, y=0.0, heading=0.0, v=0.0):
    def __init__(self, eg, sh, lattice, pl, park):
        # self.k = 0.5
        # 2022 12 20
        self.k = 0.1 # kcity
        # self.Lfc =2.0
        # 2022 12 20
        self.Lfc = 3.0 # kcity

        self.ego = eg
        self.shared = sh
        self.plan = pl
        self.parking = park
        self.lattice_path = lattice

        self.global_path = self.shared.global_path
        self.WB = 1.04 # wheel base
        # self.k = 0.15 #1.5
        self.lookahead_default = 4 #look-ahead default

        self.old_nearest_point_index = None

        # self.last_P_obsveh = None
        self.last_P_obsveh = 10

    # def __del__(self):
    #     self.old_nearest_point_index = None
    #     print("I'm dying")

    def run(self):
        while(1):
            try:
                if self.parking.on == "on":
                    self.parking_run()
                elif self.parking.on == "forced":
                    self.parking_run2()
                elif self.parking.on == "U_turn":
                    self.U_turn()
                elif self.parking.on == "off":
                    self.steer, speed = self.pure_pursuit()

                # return self.steer, speed
                return self.steer

            except IndexError:
                print("++++++++lat_controller+++++++++")


    def calc_distance(self, point_x, point_y):
        dx = self.rear_x - point_x
        dy = self.rear_y - point_y
        return hypot(dx, dy)

    def search_target_index(self):
        # To speed up nearest point search, doing it at only first time.
        if self.old_nearest_point_index is None: # 처음에만 실행되게끔
    # test_alpha = atan2(V_veh[1], V_veh[0])
            # dx, dy 선언에 사용된 문법은 list comprehension : https://semo-na.tistory.com/26
            dx = [self.rear_x - ix for ix in self.global_path.x] # pure pursuit: state.rear_x - cx[i]를 리스트로 저장
            dy = [self.rear_y - iy for iy in self.global_path.y] # pure pursuit: state.rear_y - cy[i]를 리스트로 저장
            ##!dx = [state.front_x - icx for icx in self.cx] # stanley
            ##!dy = [state.front_y - icy for icy in self.cy] # stanley
            d = np.hypot(dx, dy) # math.hypot은 인자 두개로 피타고라스 조져버리고 값 반환함

            ind = np.argmin(d) # ind = np.argmin(d) # np.argmin([list])는 리스트의 최솟값의 index를 반환함
            self.old_nearest_point_index = ind # 가장 가까운 point의 index를 저장, 이제 본 if문은 다시 실행되지 않음



        else: # 첫 실행 다음부터
            ind = self.old_nearest_point_index # 가장 가까웠던 point의 index를 저장
            distance_this_index = self.calc_distance(self.global_path.x[ind], # 줄바꿈은 가독성을 위해; 별 의미 없음
                                                      self.global_path.y[ind]) # 차량 뒷바퀴축 중심과 가장 가까웠던 point 간 거리 계산하여 저장
            while ind + 1 < len(self.global_path.x):

                distance_next_index = self.calc_distance(self.global_path.x[ind + 1], ##? 인덱스 초과 오류로 인해 ind + 1가 경로 전체 길이보다 작을 때만 작동하도록 제한함. 줄바꿈은 가독성을 위해; 별 의미 없음
                                                          self.global_path.y[ind + 1]) # 차량 뒷바퀴축 중심과 다음 point간 거리 계산하여 저장
                if distance_this_index < distance_next_index: # 물리적으로 이전 index의 point에 가까우면
                    break # while문 탈출
                # print("ind+=1")
                ind = ind + 1 if (ind + 1) < len(self.global_path.x) else ind # ind가 리스트 크기보다 커지지 않게 제한 / if else 문법 : https://wotres.tistory.com/entry/python-for-%EB%AC%B8-if-%EB%AC%B8-%ED%95%9C-%EC%A4%84-%EC%BD%94%EB%94%A9-%ED%95%98%EB%8A%94%EB%B2%95
                distance_this_index = distance_next_index # distance_this_index 최신화
            self.old_nearest_point_index = ind # self.old_nearest_point_index 최신화

        Lf = self.k * self.ego.speed + self.Lfc  # update look ahead distance

        # search look ahead target point index
        while Lf > self.calc_distance(self.global_path.x[ind], self.global_path.y[ind]):
            if (ind + 1) >= len(self.global_path.x):
                break  # not exceed goal
            ind += 1
        #############################
        # Lf = 3
        #############################
        return ind, Lf

    def pure_pursuit(self):

        heading = self.ego.heading

        # wrong
        # self.rear_x = self.ego.x - ((self.WB/2) * cos(np.radians(heading)))
        # self.rear_y = self.ego.y - ((self.WB/2) * sin(np.radians(heading)))
        # feedback
        self.rear_x = self.ego.x
        self.rear_y = self.ego.y

        ind, Lf = self.search_target_index() # trajectory에 target_course, 여기에 search_target_index 함수 적용. 이 때 현재 상태(state)를 기준으로함.     #i.e. 아래 main()에서 197번 줄 반복문을 통해 위의 Lf = k * state.v + Lfc값을 갱신하고, ind를 계속 찾는 역할을 함
        #if pind >= ind: # pind에 target_ind, 현재 계산된 인덱스(ind)가 더 앞쪽에 있을 때만 바꾼다 이 소리(즉, 현재 ind가 과거 어떤 지점의 ind보다 작으면 굳이 바꾸지 않음. <- 바꾸면 역행함.)
            #ind = pind # i.e. 비교 후 인덱스를 둘 중 다음(큰) 것으로 갱신

        # ind = self.ego.index + 50
        # Lf = 10

        print("ind : ", ind)

        tx = self.global_path.x[ind] #i.e. tx = target_course.cx[ind], tx는 현재 가는 바라본 곳의 x좌표
        ty = self.global_path.y[ind] # 바라본 곳의 y좌표


        alpha = (np.radians(heading) - atan2(ty - self.rear_y, tx - self.rear_x)) # 기하학적 관계식
        steer = np.degrees(atan2(2.0 * self.WB * sin(alpha) / Lf, 1.0)) #pure pursuit 알고리즘에 의한 식
        speed = 20
###########################junmyeong_Gay##############################
        
        # 인력장 벡터
        att_vect = np.subtract([self.global_path.x[ind], self.global_path.y[ind]], [self.ego.x, self.ego.y])
        # 인력장 헤딩(단위: degree)
        att_heading = np.degrees(atan2(att_vect[1], att_vect[0]))

        # 장애물 인덱스(global path 기준)
        obs_ind = 1500
        P_obs = [self.global_path.x[obs_ind], self.global_path.y[obs_ind]]
        # print("P_obs = ", P_obs)
        # print("P_veh = ", self.ego.x, self.ego.y)
        # print(P_obs[0]*self.ego.y-P_obs[1]*self.ego.x)
        # 장애물 속도
        V_obs = [0, 0]


        n2_w = get_n2_w(self.ego, P_obs, att_heading)
        force_potential_field, last_P_obsveh = get_f_rep(self.ego, P_obs, V_obs, n2_w)
        self.last_P_obsveh = last_P_obsveh

        theta = ss2f(self.ego.speed, self.ego.heading, force_potential_field)
    
        steer = steer + 0.4*theta
        steer = np.clip(steer, -27.0, 27.0)
        


#########################################################################################################################
        return steer, speed

    def parking_run(self):

        if self.parking.direction == 0:
            self.path = self.parking.forward_path
            lookahead = 5
        else:
            self.path = self.parking.backward_path
            lookahead = 5

        target_index = lookahead + self.parking.index
        
        target_x, target_y = self.path.x[target_index], self.path.y[target_index]
        tmp = degrees(atan2(target_y - self.ego.y, target_x - self.ego.x)) % 360

        heading = degrees(self.ego.heading)

        ###### Back Driving ######
        if self.ego.target_gear == 2:
            heading += 180
            heading %= 360
        ##########################

        alpha = heading - tmp
        angle = atan2(2.0 * self.WB *
                      sin(radians(alpha)) / lookahead, 1.0)

        ###### Back Driving ######
        if self.ego.target_gear == 2:
            angle = -1.5*angle
        ##########################

        if degrees(angle) < 3.5 and degrees(angle) > -3.5:
            angle = 0

        self.steer = max(min(degrees(angle), 27.0), -27.0)

    def parking_run2(self):
        self.steer = self.ego.target_steer

