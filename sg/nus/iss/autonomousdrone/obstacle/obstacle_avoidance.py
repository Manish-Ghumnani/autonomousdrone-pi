import time
import math

from sg.nus.iss.autonomousdrone.thread.stoppable_thread import StoppableThread
from sg.nus.iss.autonomousdrone.flight.flight_commands import FlightCommands
from sg.nus.iss.autonomousdrone.sensors.sensors import Sensors
from sg.nus.iss.autonomousdrone.flight.flight_data import FlightData


class ObstacleAvoidance(StoppableThread):
    # Class constants
    LEFT = "left"
    RIGHT = "right"
    FRONT = "front"
    REAR = "rear"

    CAUTION_DISTANCE = 200
    
    #Define all the sensors
    LEFT_SENSOR = "leftSensor"
    RIGHT_SENSOR = "rightSensor"
    FRONT_SENSOR = "frontSensor"
    REAR_SENSOR = "rearSensor"

    def __init__(self,vehicle):
        StoppableThread.__init__(self)


        self.__flight_commands = FlightCommands(vehicle)
        self.__sensors = Sensors()
        self.__flight_data = FlightData(vehicle)
        
       
        self.__illegal_input_counter = 0
        self.__last_input_legitimacy = True

  
    def run(self):
        while not self.stopped():

            try:

                print("-----------------------------------------------------------")
                #read the distance from front sensor
                ahead_distance = self.__get_sensor_reading(self.FRONT_SENSOR)

                #read the distance from rear sensor
                rear_distance = self.__get_sensor_reading(self.REAR_SENSOR)
                print("Distance Front: %d, Distance Rear: %d" % (ahead_distance, rear_distance))

                # Get a reading from the left side sensor.
                left_side_distance = self.__get_sensor_reading(self.LEFT_SENSOR)
                
                # Get a reading from the right side sensor.
                right_side_distance = self.__get_sensor_reading(self.RIGHT_SENSOR)
                print("Distance Left: %d, Distance Right: %d" % (left_side_distance, right_side_distance))

                


                if (ahead_distance >= self.CAUTION_DISTANCE) and  (rear_distance >= self.CAUTION_DISTANCE) and (left_side_distance >= self.CAUTION_DISTANCE) and (right_side_distance >= self.CAUTION_DISTANCE):
                    self.__flight_commands.maintain_altitude()
                    print ("LOITER")
                    continue
                elif(ahead_distance<=self.CAUTION_DISTANCE):
                        #then we will move rear
                        #before check the distance from rear sensor
                        if(rear_distance>=self.CAUTION_DISTANCE):
                             self.__move_in_direction(self.REAR)
                           
                        else:
                            #move left or right
                            #first check for the left sensor:
                            if(left_side_distance>=self.CAUTION_DISTANCE):
                                 self.__move_in_direction(self.LEFT)
                                
                            elif(right_side_distance>=self.CAUTION_DISTANCE):
                                 self.__move_in_direction(self.RIGHT)
                                
                            else:
                                self.__flight_commands.maintain_altitude()
                                print("Way is clear you are free to move")
                                print("LOITER")


                elif(rear_distance<=self.CAUTION_DISTANCE):
                    #then we will move ahead
                    #before check the distance from ahead sensor
                    if(ahead_distance>=self.CAUTION_DISTANCE):
                         self.__move_in_direction(self.FRONT)
                       
                    else:
                        #move left or right
                        #first check for the left sensor:
                        if(left_side_distance>=self.CAUTION_DISTANCE):
                             self.__move_in_direction(self.LEFT)
                           
                        elif(right_side_distance>=self.CAUTION_DISTANCE):
                             self.__move_in_direction(self.RIGHT)
                            
                        else:
                            self.__flight_commands.maintain_altitude()
                            print("Way is clear you are free to move")
                            print("LOITER")


                elif(left_side_distance<=self.CAUTION_DISTANCE):
                    #then we will move right
                    #before check the distance from right sensor from caution_distance
                    if(right_side_distance>=self.CAUTION_DISTANCE):
                        self.__move_in_direction(self.RIGHT)
                        print("Move RIGHT....")
                    else:
                        #move left or right
                        #first check for the left sensor:
                        if(ahead_distance>=self.CAUTION_DISTANCE):
                            self.__move_in_direction(self.RIGHT)
                            
                        elif(rear_distance>=self.CAUTION_DISTANCE):
                            self.__move_in_direction(self.REAR)
                            
                        else:
                           print("Way is clear you are free to move")
                           print("LOITER")
                   
                
                elif(right_side_distance<=self.CAUTION_DISTANCE):
                    #then we will move left
                    #before check the distance from left side to caution distance
                    if(left_side_distance>=self.CAUTION_DISTANCE):
                        self.__move_in_direction(self.LEFT)
                        
                    else:
                        #move ahead or rear
                        #first check for the ahead sensor:
                        if(ahead_distance>=self.CAUTION_DISTANCE):
                            self.__move_in_direction(self.AHEAD)
                           
                        elif(rear_distance>=self.CAUTION_DISTANCE):
                            self.__move_in_direction(self.REAR)
                           
                        else:
                            print("Way is clear you are free to move")
                            print("LOITER")

                else:
                    print("Way is clear you are free to move")
                    print("LOITER")

                continue
            except KeyboardInterrupt:
                self.__flight_commands.land()
                print("Landed Successfully...")
                self.stopit()
                system.exit(1)
 

    def __move_in_direction(self, direction):
        if direction == self.RIGHT:
            self.__flight_commands.go_right()

        elif direction == self.LEFT:
            self.__flight_commands.go_left()

        elif direction == self.REAR:
            self.__flight_commands.go_back()
        
        elif direction == self.FRONT:
            self.__flight_commands.go_front()
        
        elif direction == self.UP:
            self.__flight_commands.go_up()
            self.__keep_altitude = True
            self.__start_time_measure = round(time.time())

        elif type(direction).__name__ is "str":
            raise ValueError('Expected "' + self.AHEAD + '" / "' + self.LEFT + '" / "' + self.RIGHT + '", instead got ' +
                             str(direction))
        else:
            raise TypeError('Expected variable of type str and got a variable of type ' + type(direction).__name__)


    def __get_sensor_reading(self, sensor):
        legal_input = False
        while legal_input is False:
            if sensor is self.FRONT_SENSOR:
                distance = self.__sensors.check_ahead()

            elif sensor is self.RIGHT_SENSOR:
                distance = self.__sensors.check_right_side()

            elif sensor is self.LEFT_SENSOR:
                distance = self.__sensors.check_left_side()

            elif sensor is self.REAR_SENSOR:
                distance = self.__sensors.check_below()

            else:
                if isinstance(sensor, str):
                    raise ValueError('Expected "' + self.FRONT_SENSOR + '" / "' + self.REAR_SENSOR + '" / "' +
                                     self.LEFT_SENSOR + '" / "' + self.RIGHT_SENSOR + '", instead got ' + sensor)
                else:
                    raise TypeError('Expected variable of type str and got a variable of type ' + type(sensor).__name__)

            legal_input = self.__check_measurement( int(distance))
            if legal_input:
                return distance

    def __check_measurement(self, measurement):
        is_int = isinstance(measurement, int)

        if is_int is False and measurement is not "NACK":
            raise TypeError('Expected variable of type int and got a variable of type ' + type(measurement).__name__)

        if is_int:
            if measurement > 0:
                self.__last_input_legitimacy = True
                return True

        if self.__last_input_legitimacy is True:
            self.__illegal_input_counter = 1
        else:
            self.__illegal_input_counter += 1
            if self.__illegal_input_counter >= 10:
                raise SystemError('Malfunction in sensors, check physical connections')


        self.__last_input_legitimacy = False
        return False


    def take_control(self):
        return self.__is_active
