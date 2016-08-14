import RPi.GPIO as GPIO
import time

class LED:

    def init_common(self,pin):
        self.GPIO_NO=pin
        GPIO.setwarnings(False)	# Suppress warnings
        GPIO.setmode( GPIO.BOARD )
        GPIO.setup( self.GPIO_NO, GPIO.OUT )

    def __init__(self,pin_no=12):
        """LED(pin_no) pin_no is pin number (not GPIP number)
        """
        self.init_common(pin_no)

    def set(self,is_on):
        GPIO.output( self.GPIO_NO, is_on )

