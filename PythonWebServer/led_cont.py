import RPi.GPIO as GPIO
import time

class LED:

    def init_common(self,pin):
        self.GPIO_NO=pin
        GPIO.setwarnings(False)	# Suppress warnings
        GPIO.setmode( GPIO.BCM )
        GPIO.setup( self.GPIO_NO, GPIO.OUT )

    def __init__(self,pin):
        self.init_common(pin)

    def __init__(self):
        self.init_common(21) #GPIO 21, PIN 40

    def set(self,is_on):
        GPIO.output( self.GPIO_NO, is_on )

