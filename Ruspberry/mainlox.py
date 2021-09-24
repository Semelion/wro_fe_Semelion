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

#img_size = [640,480]
def linepoz(img):
    img = img[180:, :]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.GaussianBlur(hsv, (3,3), 0)
    or_min = np.array((0, 0, 0), np.uint8)
    or_max = np.array((62, 140, 225), np.uint8)
    orange = cv.inRange(hsv, or_min, or_max)
    i = 0
    cv.imshow('lineblack', line)
    contours0, hierarchy = cv.findContours(orange.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    color=0
    Line = 0
    for cnt in contours0:
        perimeter = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
        if perimeter > 300 and perimeter <5000:
            #print(perimeter)
            Line = 1
            approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
            #cv.drawContours(img, [cnt], 0, (0,0, 255), 2)  #
    #cv.imshow('line', img)
    return Line

# ввод изображение
# вывод color (0 нет цветов,1 зеленый, 2 красный) )
def town(img):
    img = img[220:, :]
    img = cv.GaussianBlur(img, (3,3), 0)
    #bl_min = np.array((40, 75, 0), np.uint8)
    #bl_max = np.array((88, 255, 75), np.uint8)
    #thresh = cv.inRange(img, bl_min, bl_max)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh = np.zeros_like(img)
    thresh[(img < 24)] = 255
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
max = 0
while number <= 4:
    ret,frame = cap.read()
    img = frame[:370,:]
    e = town(img)
    e = int(e * 0.5 + 25 )
    if e >= 95:
        e = 100
    elif e <= 5:
        e = 0
    print(e,"err")
    servo = 19
    GPIO.setup(servo, GPIO.OUT)
    setServoAngle(servo, e)
    ch = cv.waitKey(5)
    if ch == 27:
        break
    n = linepoz(img)
    max = max + n
    print(max)
cv.destroyAllWindows()