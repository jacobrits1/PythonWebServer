import RPi.GPIO as GPIO
import time
"""http://om.hatenablog.com/entry/2015/02/14/204009

GPIO17 = Pin 11
GPIO18 = Pin 12 
GPIO22 = Pin 15
GPIO23 = Pin 16
"""
class LED_PWM:
    """LED_PWM(pin_no) Tested 11,12,15,16
    """
    def __init__(self, pin_no):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_no, GPIO.OUT)
        self.p = GPIO.PWM(pin_no, 150)
        self.p.start(0)
    def lite(self,percent):
        """lite(percent) percent = 0 .. 100
        """
        if percent < 0:
            percent = 0
        elif percent > 100:
            percent = 100
        self.p.ChangeDutyCycle(percent)
    def demo(self,nn):
        """demo() nn times  0% to 100%  -> 100% to 0%
        """
        for ii in range(0,nn):
            for dc in range(0, 101, 5):
                self.main(dc)
                time.sleep(0.1)
            for dc in range(100, -1, -5):
                self.main(0)
                time.sleep(0.1)
