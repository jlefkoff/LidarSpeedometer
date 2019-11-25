import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM) # Use physical pin numbering
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Se t pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True: # Run forever
	right = GPIO.input(13)
        mid = GPIO.input(6)
        left = GPIO.input(5)
        back = GPIO.input(18)
        if right == False:
		print("right was pushed!")
                time.sleep(.35)
        elif mid == False:
                print("mid was pushed!")
                time.sleep(.35)
        elif left == False:
                print("left was pushed!")
                time.sleep(.35)
        elif back == False:
                print("back was pushed!")
                time.sleep(.35)
