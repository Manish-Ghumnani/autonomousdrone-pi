from obstacle_avoidance_modified import ObstacleAvoidance
from vehicle import Vehicle
import time

vehicle = Vehicle()
print("I am After Vehicle")
try:
    obstacle_avoidance_system = ObstacleAvoidance(vehicle)
    obstacle_avoidance_system.start()
    flag = True
except KeyboardInterrupt:
     system.exit(1)
##while flag:
##    time.sleep(0.1)
##    if obstacle_avoidance_system.take_control():
##        print("override")
##
##    if obstacle_avoidance_system.isAlive() is False:
##        flag = False
##        print("Terminated")
