import pymap3d as pm

base_lat = 37.45107175
base_lon = 126.6494964
base_alt = 15.4

def get_xy(lat, lon, alt):  # 점들 사이의 새로운 점들을 설정
    e, n, u = pm.geodetic2enu(lat, lon, alt, base_lat, base_lon, base_alt)
    print("hello")
    return e, n

x = 37.4509271053147
y = 126.649281872579
z = 1

x, y = get_xy(x,y,z)

print('x : {0}, y : {1}'.format(x,y))