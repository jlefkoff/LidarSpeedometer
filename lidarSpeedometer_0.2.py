#!/usr/bin/env python
#By jonah lefkoff 2019
import RPi.GPIO as GPIO
import time
import statistics
from time import sleep
from lidar_lite import Lidar_Lite
from firebase import firebase

lidar = Lidar_Lite()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

segmentClock=17
segmentLatch=27
segmentData=22
rightButton=13
midButton=6
leftButton=5
backButton=18

GPIO.setup(segmentClock, GPIO.OUT)
GPIO.setup(segmentData, GPIO.OUT)
GPIO.setup(segmentLatch, GPIO.OUT)
GPIO.setup(rightButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(leftButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(midButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(backButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(segmentClock,GPIO.LOW)
GPIO.output(segmentData,GPIO.LOW)
GPIO.output(segmentLatch,GPIO.LOW)


firebase= firebase.FirebaseApplication('https://lidarspeedometer.firebaseio.com/') #init database

seconds = 1545925769.9618232
today  = time.ctime(seconds) #for database (date & time)

number=0

connected = lidar.connect(1) #connect lidar

#Takes a number and displays 2 numbers. Display absolute value (no negatives)
#look here maybe bug between value+number
def showNumber(value):
            number = abs(value) #Remove negative signs and any decimals
            x=0
            while(x<2):
                remainder=number % 10
                postNumber(remainder)
                number /= 10
                x += 1

            GPIO.output(segmentLatch,GPIO.LOW)
            GPIO.output(segmentLatch,GPIO.HIGH)


def postNumber(number):
    a=1<<0
    b=1<<6
    c=1<<5
    d=1<<4
    e=1<<3
    f=1<<1
    g=1<<2
    dp=1<<7

    if   number == 1: segments =     b | c
    elif number == 2: segments = a | b |     d | e |     g
    elif number == 3: segments = a | b | c | d |         g
    elif number == 4: segments =     b | c |         f | g
    elif number == 5: segments = a |     c | d     | f | g
    elif number == 6: segments = a |     c | d | e | f | g
    elif number == 7: segments = a | b | c
    elif number == 8: segments = a | b | c | d | e | f | g
    elif number == 9: segments = a | b | c | d     | f | g
    elif number == 0: segments = a | b | c | d | e | f
    elif number == ' ': segments = 0
    elif number == 'c': segments = g | e | d
    elif number == '-': segments = g
    else: segments  = False

    y=0
    while(y<8):
        GPIO.output(segmentClock,GPIO.LOW)
        GPIO.output(segmentData,segments & 1 << (7-y))
        GPIO.output(segmentClock,GPIO.HIGH)
        y += 1

x=0
while True:
    rightButtonPos = GPIO.input(rightButton)
    midButtonPos = GPIO.input(midButton)
    leftButtonPos = GPIO.input(leftButton)
    backButtonPos =GPIO.input(backButton)
    if backButtonPos == True: #user ID input
        if midButtonPos == False:
            x+=1
            postNumber(x)
            sleep(.2)
        else:
            postNumber(x)
    else:
        for y in range(5, 0, -1): #countdown
            showNumber(y)
            time.sleep(0.9)
        vel = lidar.getVelocity() #get lidar data
        dist = lidar.getDistance()
        velPos = abs(vel) #clean up data
        if velPos > 99: # ''
            velPos %= 10
        velPos *= 1.60934 #in MPH
        velPos = round(velPos)
        speedList = [velPos]
        for z in range(0, 5, 1):
            vel = lidar.getVelocity() #get lidar data
            dist = lidar.getDistance()
            velPos = abs(vel) #clean up data
            if velPos > 99: # ''
                velPos %= 10
            velPos *= 1.60934 #in MPH
            velPos = round(velPos)
            speedList.append(velPos)
        velAvg = statistics.mean(speedList)
        velAvg = round(velAvg)
        showNumber(velAvg) #print to display
        firebase.post('/data', { "Distance":str(dist), "velocity":str(velAvg), "User ID":x, "Date":today}) #post to database
        time.sleep(2)
GPIO.cleanup()
