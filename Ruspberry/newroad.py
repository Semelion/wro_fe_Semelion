import numpy as np
import cv2 as cv
import math
import serial
from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
def setServoAngle(servo, angle):
    pwm = GPIO.PWM(servo, 50)
    pwm.start(8)
    dutyCycle = angle / 18. + 3.
    pwm.ChangeDutyCycle(dutyCycle)
    sleep(0.02)
    dutyCycle = 0
#arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

'''
import serial

time.sleep(1)
cc=str(arduino.readline())
print(cc[2:][:-5])
arduino.flushInput()
'''

#img_size = [640,480]
def linepoz(img):
    img = img[190:, :]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.GaussianBlur(hsv, (3,3), 0)
    b_min = np.array((83, 97, 43), np.uint8)
    b_max = np.array((255, 255, 130), np.uint8)
    blue = cv.inRange(hsv, b_min, b_max)
    or_min = np.array((0, 0, 68), np.uint8)
    or_max = np.array((68, 255, 130), np.uint8)
    orange = cv.inRange(hsv, or_min, or_max)
    line = blue + orange
    i = 0
    Line = 0
    cv.imshow('lineblack', line)
    while i < 2:
        i = i + 1
        if i == 1:
            contours0, hierarchy = cv.findContours(blue.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        else:
            contours0, hierarchy = cv.findContours(orange.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        color=0
        for cnt in contours0:
            perimeter = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
            if perimeter > 700 and perimeter <5000:
                #print(perimeter)
                Line = i
                approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
                cv.drawContours(img, [cnt], 0, (0,0, 255), 2)  #
    #cv.imshow('line', img)
    return Line

# ввод изображение
# вывод color (0 нет цветов,1 зеленый, 2 красный) )
def town(img):
    img = img[160:, :]
    img = cv.GaussianBlur(img, (3,3), 0)
    #bl_min = np.array((40, 75, 0), np.uint8)
    #bl_max = np.array((88, 255, 75), np.uint8)
    #thresh = cv.inRange(img, bl_min, bl_max)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img1 = img
    hsv = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
    hsv = cv.GaussianBlur(hsv, (3, 3), 0)

    r_min = np.array((0, 60, 45), np.uint8)
    r_max = np.array((26, 255, 83), np.uint8)
    red = cv.inRange(hsv, r_min, r_max)
    gr_min = np.array((60, 160, 38), np.uint8)
    gr_max = np.array((82, 255, 100), np.uint8)
    green = cv.inRange(hsv, gr_min, gr_max)
    town = red + green
    thresh = np.zeros_like(img)
    thresh[(img < 19)] = 255
    red_sum = np.sum(red)
    green_sum = np.sum(green)
    thresh = thresh
    leftt = thresh[:,:240]
    rightt = thresh[:, 400:]
    left_sum = np.sum(leftt)
    right_sum = np.sum(rightt)
    l= 0
    r = 240
    il,ir = 0,0
    ld ,rd = 0,0
    while il == 0 or ir == 0:
        l = l + 1
        r = r-1
        left = leftt[:, l:]
        right = rightt[:,:r]
        left_sum = np.sum(left)
        right_sum = np.sum(right)
        if il == 0 and left_sum < 100:
            il = 1
            ld = l
        if ir == 0 and right_sum < 100:
            ir = 1
            rd = 240 - r
            rd = int(rd * 1.28)
    if red_sum > 700000 or green_sum > 700000:
        if red_sum > green_sum:
            ld = ld + 50
        else:
            rd = rd + 50
    print(ld,rd)
    err = int(ld - rd)
    #print(err,"err")
    #print(left_sum,right_sum)
    #leftt = thresh[:,400:640-76]
    cv.imshow('thresh', thresh)
    if il == 0:
        cv.imshow('left', leftt)
    if ir == 0:
        cv.imshow('right', rightt)
    return err
cap = cv.VideoCapture(0)
line = 0
number = 0
n = 0
while number <= 4:
    ret,frame = cap.read()
    img = frame[:320,:]
    #line = linepoz(img)
    e = town(img)
    e = int(e * 0.5 + 10 )
    if e >= 95:
        e = 100
    elif e <= 5:
        e = 0
    print(e,"err")
    #rint(color,"color")
    servo = 19
    GPIO.setup(servo, GPIO.OUT)
    setServoAngle(servo, e)
    ch = cv.waitKey(5)
    if ch == 27:
        break
    #if line == 1 or line == 2:
        #n = n + 1
    #print(n,"n")



