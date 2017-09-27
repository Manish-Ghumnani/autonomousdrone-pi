from Ultrasonic import Sonar

class Sensors:

    def __init__(self):
        self.__left_sensor = Sonar(23,24,1)
        self.__front_sensor = Sonar(26,19,2)
        self.__right_sensor = Sonar(17,27,3)
        self.__below_sensor = Sonar(20,21,4) #it means rear sensor

    # Returns distance measurement from the front sensor
    def check_ahead(self):
        ahead_read = self.__front_sensor.get_distance()
##        if ahead_read <= 0 or ahead_read > 200:  # This is the the CAUTION DISTANCE from ObstacleAvoidance class.
##            #simulator.skip()
        return ahead_read

    # Returns distance measurement from the left sensor
    def check_left_side(self):
        left_side_read = self.__left_sensor.get_distance()
        return left_side_read

    # Returns distance measurement from the right sensor
    def check_right_side(self):
        right_side_read = self.__right_sensor.get_distance()
        return right_side_read

    # Returns distance measurement from the sensor below.
    def check_below(self):
        below_read = self.__below_sensor.get_distance()
        return below_read
