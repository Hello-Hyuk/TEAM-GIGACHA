#!/bin/bash
#!/user/bin/env pythonnoetic
#chmod -rf 777
#chmod 777 /dev/erp42
#chmod +x ~/TEAM-GIGACHA/src/planner_and_control/script
echo Process started...
#echo obstacle avoidance?[y/n]
#read obs
python3 serial_io.py & python3 mission_planner.py & python3 behavior_planner.py & python3 motion_planner.py & python3 controller.py & python3 sensor_hub.py
#if [ $obs == "y" ];then
#       python3 serial_io.py & python3 mission_planner.py & python3 behavior_planner.py & python3 motion_planner.py & python3 controller.py & python3 sensor_hub.py & python3 input.py
#else 
#       python3 serial_io.py & python3 mission_planner.py & python3 behavior_planner.py & python3 motion_planner.py & python3 controller.py & python3 sensor_hub.py 
#fi
