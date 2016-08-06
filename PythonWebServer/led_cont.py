import RPi.GPIO as GPIO
import time
#ptvsd
#ptvsd.enable_attach('test')

GPIO_NO = 21
#PIN 40

def init_led():
    GPIO.setwarnings(False)	# Suppress warnings
    GPIO.setmode( GPIO.BCM )
    GPIO.setup( GPIO_NO, GPIO.OUT )

def set_led(is_on):
	GPIO.output( GPIO_NO, is_on )

