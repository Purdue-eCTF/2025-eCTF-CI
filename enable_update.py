import RPi.GPIO as GPIO
import time
GPIO_PIN = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.OUT)

GPIO.output(GPIO_PIN, GPIO.LOW)
