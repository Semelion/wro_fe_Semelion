import numpy as np
import cv2 as cv
import math
'''
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)

arduino.write(bytes("start", 'utf-8'))
time.sleep(1)
cc=str(arduino.readline())
print(cc[2:][:-5])
arduino.flushInput()

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=60,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )
cap = cv.VideoCapture(gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)'''
#img_size = [1280,720]

# ввод изображение
# вывод color (0 нет цветов,1 зеленый, 2 красный) )
def town(img):
    img = img[60:, :]
    img1 = img.copy()
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.erode(hsv, None, iterations=4)
    r_min = np.array((0, 0, 0), np.uint8)
    r_max = np.array((20, 255, 255), np.uint8)
    red = cv.inRange(hsv, r_min, r_max)
    gr_min = np.array((0, 120, 30), np.uint8)
    gr_max = np.array((80, 255, 100), np.uint8)
    green = cv.inRange(hsv, gr_min, gr_max)
    town = red + green
    contours0, hierarchy = cv.findContours(town.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    color=0
    cv.imshow('townd', town)
    for cnt in contours0:
        rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
        box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
        box = np.int0(box)  # округление координат
        edge1 = np.int0((box[1][0] - box[0][0],box[1][1] - box[0][1]))
        edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))
        usedEdge = edge1
        if cv.norm(edge2) > cv.norm(edge1):
            usedEdge = edge2
        reference = (1,0)
        perimeter = cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
        if len(approx) == 4:
            angle = 180.0 / math.pi * math.acos((reference[0]*usedEdge[0]+ reference[1]*usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
        else:
            angle = 0.0
        #print("usedadge",angle)
        distance = 0
        if perimeter > 200 and  perimeter < 600 and len(approx) == 4 and angle > 85 and angle < 95:
            #print(perimeter)
            approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
            y10 = approx[0][0][0]
            y11 = approx[1][0][0]
            y20 = approx[2][0][0]
            y21 = approx[3][0][0]
            x10 = approx[0][0][1]
            x11 = approx[3][0][1]
            x20 = approx[1][0][1]
            x21 = approx[2][0][1]
            y1 = int((y10 + y11)/2)
            y2 = int((y20 + y21) / 2)
            x1 = int((x10 + x11) / 2)
            x2 = int((x20 + x21) / 2)
            red_sum = np.sum(red[x1:x2,y1:y2])
            green_sum = np.sum(green[x1:x2,y1:y2])
            #print(green_sum + red_sum )
            sum = green_sum + red_sum
            if sum > 10000000:
                color = 0
                g_color = 0
                r_color = 0
            elif green_sum > red_sum:
                color = 2
                g_color = 255
                r_color = 0
            else :
                color = 1
                r_color = 255
                g_color = 0
                #print("red")
            cv.drawContours(img, [box], 0, (0, g_color, r_color), 2)  #
    cv.imshow('town', img)
    img = img1
    return color

def townwithline(img1,line):
    if line == 2:
        img1 = img1[60:, 190:]
        img = img1[:, :50]
        dis = 50
    elif line == 1:
        img1 = img1[60:, :600]
        img = img1[:, 650:]
        dis = 650
    dif = 0
    cv.imshow('towend', img1)
    while dif == 0 and dis > 0 and dis < 450:
        if line == 2:
            dis = dis + 50
            img = img1[:, :dis]
        elif line == 1:
            dis = dis - 50
            img = img1[:, dis:]
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        r_min = np.array((0, 0, 0), np.uint8)
        r_max = np.array((20, 255, 255), np.uint8)
        red = cv.inRange(hsv, r_min, r_max)
        gr_min = np.array((60, 180, 40), np.uint8)
        gr_max = np.array((88, 255, 206), np.uint8)
        green = cv.inRange(hsv, gr_min, gr_max)
        town = red + green
        contours0, hierarchy = cv.findContours(town.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        color=0
        cv.imshow('townd', town)
        for cnt in contours0:
            rect = cv.minAreaRect(cnt)  # пытаемся вписать прямоугольник
            box = cv.boxPoints(rect)  # поиск четырех вершин прямоугольника
            box = np.int0(box)  # округление координат
            edge1 = np.int0((box[1][0] - box[0][0],box[1][1] - box[0][1]))
            edge2 = np.int0((box[2][0] - box[1][0], box[2][1] - box[1][1]))
            usedEdge = edge1
            if cv.norm(edge2) > cv.norm(edge1):
                usedEdge = edge2
            reference = (1,0)
            perimeter = cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)

            if len(approx) == 4:
                angle = 180.0 / math.pi * math.acos((reference[0]*usedEdge[0]+ reference[1]*usedEdge[1]) / (cv.norm(reference) * cv.norm(usedEdge)))
                #print(perimeter,angle)
                #cv.drawContours(img1, [box], 0, (0, 255, 255), 2)  #
            else:
                angle = 0.0
            #print("usedadge",angle)
            distance = 0
            if perimeter > 69 and  perimeter < 300 and len(approx) == 4 and angle >= 65 and angle < 100:
                dif = dif+1
                #print(perimeter,angle)

                approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
                y10 = approx[0][0][0]
                y11 = approx[1][0][0]
                y20 = approx[2][0][0]
                y21 = approx[3][0][0]
                x10 = approx[0][0][1]
                x11 = approx[3][0][1]
                x20 = approx[1][0][1]
                x21 = approx[2][0][1]
                y1 = int((y10 + y11)/2)
                y2 = int((y20 + y21) / 2)
                x1 = int((x10 + x11) / 2)
                x2 = int((x20 + x21) / 2)
                red_sum = np.sum(red[x1:x2,y1:y2])
                green_sum = np.sum(green[x1:x2,y1:y2])
                #print(green_sum + red_sum )
                sum = green_sum + red_sum
                if sum > 10000000:
                    color = 0
                    g_color = 0
                    r_color = 0
                elif green_sum > red_sum:
                    color = 2
                    g_color = 255
                    r_color = 0
                    break
                else :
                    color = 1
                    r_color = 255
                    g_color = 0
                    #print("red")
                    break
                cv.drawContours(img, [box], 0, (0, g_color, r_color), 2)  #

    cv.imshow('town', img)
    img = img1
    return color
# ввод изображение
# вывод Line (0 нет линий,1 синия, 2 оранжевая) )
def linepoz(img):
    img = img[110:, :]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    hsv = cv.erode(hsv, None, iterations=4)
    b_min = np.array((50, 0, 30), np.uint8)
    b_max = np.array((255, 75, 90), np.uint8)
    blue = cv.inRange(hsv, b_min, b_max)
    or_min = np.array((0, 0, 40), np.uint8)
    or_max = np.array((40, 80, 130), np.uint8)
    orange = cv.inRange(hsv, or_min, or_max)
    line = blue + orange
    i = 0
    Line = 0
    cv.imshow('imgg', line)
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
            if perimeter > 800 and perimeter <5000:
                #print(perimeter)
                Line = i
                approx = cv.approxPolyDP(cnt, 0.04 * perimeter, True)
                cv.drawContours(img, [cnt], 0, (0,0, 255), 2)  #
    cv.imshow('img', img)
    return Line

line = 0
while True:
    while line == 0:
        a = input()
        img = cv.imread( a + ".png")
        img = img[:360, :]
        line = linepoz(img)
        color = townwithline(img,2)
        #print(line,"line")
        print(color,"color")
        #отправить color на ардуино
        ch = cv.waitKey(5)
        if ch == 27:
            break
    # как увидим линию остановка и считываем кубики
    color_turn = townwithline()
    # color_turn отправляем на ардуинку если равна одному едим до стенки и поворот если 2 едим чуть и поворачиваем
