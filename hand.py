import cv2
import numpy as np
import math
import os
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

count = 0
mod = 0
card = 0
data = []
fingers = []
x_prev = 0
y_prev = 0
x_offset = 150
y_offset = 150
start = False
first = False
driver = 0
homePage = "http://www.google.com/"

cap = cv2.VideoCapture(0)
backSub = cv2.createBackgroundSubtractorMOG2(history=500,
                                             varThreshold=16,
                                             detectShadows=True)


def find_move(data_arr, fingers_arr):
    fingers_num = 0
    if data_arr[0] > 320:
        pivot = min(data_arr)
    else:
        pivot = max(data_arr)
    n = len(data_arr)
    for i in range(n):
        data_arr[i] -= pivot
    print(data_arr, len(data_arr))
    print(fingers_arr, len(fingers_arr))
    if len(data_arr) == len(fingers_arr):
        # fingers_num = max(fingers_arr)
        fingers_num = max(set(fingers_arr), key=fingers_arr.count)
    one = []
    two = []
    found_zero = False
    for i in data_arr:
        if i == 0:
            found_zero = True
        if i != 0 and found_zero:
            two.append(i)
        elif i != 0:
            one.append(i)
    print(one, two)
    if len(one) + len(two) < 5:
        return None
    if len(one) - list([a_i - b_i for a_i, b_i in
                        zip(one, sorted(one, reverse=True))]).count(
        0) < 3 and len(two) - list(
        [a_i - b_i for a_i, b_i in zip(two, sorted(two))]).count(0) < 3:
        if one and two:
            return ["right", fingers_num]
        else:
            return ["swipe right", fingers_num]
    elif len(one) - list([a_i - b_i for a_i, b_i in
                          zip(one, sorted(one))]).count(
        0) < 3 and len(two) - list(
        [a_i - b_i for a_i, b_i in zip(two, sorted(two, reverse=True))]).count(
        0) < 3:
        if one and two:
            return ["left", fingers_num]
        else:
            return ["swipe left", fingers_num]


while cap.isOpened():
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    ret = cv2.flip(ret, 1)

    fgMask = backSub.apply(img)
    mask = img.copy()

    contours, tmp = cv2.findContours(fgMask, cv2.RETR_LIST,
                                     cv2.CHAIN_APPROX_SIMPLE)

    size = i = 0
    max_points = 100000
    sensitivity = 5000

    x = y = w = h = 0
    x_average = y_average = 0

    for cnt in contours:
        i += 1
        if sensitivity < cv2.contourArea(cnt) and max_points > i:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 0), -1)
            cv2.drawContours(fgMask, [cnt], 0, (255, 255, 255), -1)
            x_average += x + w / 2
            y_average += y + h / 2
            # print(x_average, y_average)
            cv2.circle(mask, (int(x_average), int(y_average)), 5, (0, 255, 0),
                       -1)
            size += 1

    if w == 640 and h == 480:
        if start:
            print("stop")
        if first and not start:
            driver = webdriver.Firefox()
            driver.get(homePage)
            backSub = cv2.createBackgroundSubtractorMOG2(history=500,
                                                         varThreshold=16,
                                                         detectShadows=True)
            start = True
        if not first:
            first = True

    # print(size)
    if size != 0:
        x_average = x_prev = int(x_average / size)
        y_average = y_prev = int(y_average / size)
        data.append(x_average)
    else:
        x_average = x_prev
        y_average = y_prev

    crop_img = fgMask[
               max(y_average - y_offset, 0):min(y_average + y_offset, 480),
               max(x_average - x_offset, 0):min(x_average + x_offset, 640)
               ]

    value = (35, 35)
    blurred = cv2.GaussianBlur(crop_img, value, 0)
    _, thresh = cv2.threshold(blurred, 127, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)

    drawing = _
    count_defects = _
    defects = _
    cnt = _
    if contours:
        cnt = max(contours, key=lambda x: cv2.contourArea(x))
        x, y, w, h = cv2.boundingRect(cnt)
        hull = cv2.convexHull(cnt)
        drawing = np.zeros(mask.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)
        hull = cv2.convexHull(cnt, returnPoints=False)
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh, contours, -1, (0, 255, 0),
                         3)

    if hasattr(defects, 'shape') and size != 0 and start:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])
            #
            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

            if angle <= math.pi / 2:
                count_defects += 1
                cv2.circle(drawing, far, 5, [0, 0, 255], -1)
                dist = cv2.pointPolygonTest(cnt, far, True)
            # count_defects += 1
            cv2.line(drawing, start, end, [0, 255, 0], 2)
            cv2.circle(drawing, far, 5, [255, 0, 0], -1)
        fingers.append(count_defects)

    if len(data) > 1 and size == 0 and start:
        res = find_move(data, fingers)
        print(res)
        if res:
            if res[0] == "swipe left":
                driver.execute_script('''window.close();''')
                Window_List = driver.window_handles
                driver.switch_to.window(Window_List[-1])
            if res[0] == "swipe right":
                driver.execute_script('''window.open("","_blank");''')
                Window_List = driver.window_handles
                driver.switch_to.window(Window_List[-1])
                # card = (card + 1) % len(Window_List)

        data = []
        fingers = []

    cv2.imshow("fgMask", fgMask)
    cv2.imshow("mask", mask)
    # cv2.imshow('crop_img', crop_img)
    cv2.imshow("blurred", blurred)
    cv2.imshow("thresh", thresh)
    if contours:
        cv2.imshow("drawing", drawing)

    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord("q"):
        if start:
            driver.close()
        break
    if keypress == ord("r"):
        backSub = cv2.createBackgroundSubtractorMOG2(history=500,
                                                     varThreshold=16,
                                                     detectShadows=True)
