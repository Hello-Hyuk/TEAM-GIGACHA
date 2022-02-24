1. ublox_f9p, e2box 패키지를 압축 해제한다.*

<!--########ublox_f9p 패키지관련##########-->
1. /ublox_f9p/ublox_gps/launch
2. ublox_zed-f9p.launch 실행
3. port 번호 수정시 /ublox_f9p/ublox_gps/config/zed-f9p.yaml에서 /dev/gps로 되어있는지 확인
4. /ublox_f9p/ublox_gps/launch/ublox_zed-f9p.launch에서 AHRS port번호 /dev/imu로 되어있는지 확인

<!--########e2box 패키지관련##########-->
1. /e2box_AHRS/src/main.cpp에서 145번줄에 port번호 /dev/imu로 되어있는지 확인


position.py 실행