import RPi.GPIO as GPIO
import time
import threading

class Sonar:
    global distance
   
    TRIG = 0
    ECHO = 0


    def __init__(self, TRIG, ECHO,i):
       
        GPIO.setmode(GPIO.BCM)
        self.TRIG = TRIG
        self.ECHO = ECHO
        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)
        GPIO.output(self.TRIG, False)
        print ("Waiting For Sensor %d  To Settle"%(i))
        print("Connected Successfuly to Sensor %d"%(i))
        i=i+1
        time.sleep(1)
       

    def get_distance(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG, False)
        pulse_start=0
        pulse_end=0
        while GPIO.input(self.ECHO) == 0:
            pulse_start = time.time()

        while GPIO.input(self.ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = (pulse_duration * 34300) / 2

        distance = round(distance, 2)
        time.sleep(0.5)
        return distance

#######################################################################################################################
