import time

from sg.nus.iss.autonomousdrone.vehicle.vehicle import Vehicle
from sg.nus.iss.autonomousdrone.obstacle.obstacle_avoidance import ObstacleAvoidance

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
