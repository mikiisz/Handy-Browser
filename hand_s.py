import cv2
import numpy as np
import math
from selenium import webdriver


def static_camera(img_counter, fg_mask, img, sensitivity, max_points):
    cv2.rectangle(img, (600, 50), (400, 400), (0, 255, 0), 0)
    crop_img = img[50:400, 400:600]
    picture = img.copy()
    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    value = (35, 35)
    blurred = cv2.GaussianBlur(grey, value, 0)
    _, thresh1 = cv2.threshold(blurred, 127, 255,
                               cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    blank, _ = cv2.findContours(fg_mask, cv2.RETR_LIST,
                                cv2.CHAIN_APPROX_SIMPLE)

    contours, hierarchy = cv2.findContours(thresh1.copy(), cv2.RETR_TREE,
                                           cv2.CHAIN_APPROX_NONE)

    i = 0
    x_average = y_average = 0
    for cnt in blank:
        i += 1
        if sensitivity < cv2.contourArea(cnt) and max_points > i:
            (x, y, w, h) = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 0)
            x_average += x + w / 2
            y_average += y + h / 2

    cnt = max(contours, key=lambda xs: cv2.contourArea(xs))

    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 0, 255), 0)

    hull = cv2.convexHull(cnt)

    drawing = np.zeros(crop_img.shape, np.uint8)
    cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
    cv2.drawContours(drawing, [hull], 0, (0, 0, 255), 0)

    hull = cv2.convexHull(cnt, returnPoints=False)

    defects = cv2.convexityDefects(cnt, hull)
    count_defects = 0
    cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)

    if hasattr(defects, 'shape'):
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]

            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])

            a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
            b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
            c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
            angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))

            if angle <= math.pi / 2:
                count_defects += 1
                cv2.circle(crop_img, far, 1, [0, 0, 255], -1)

            cv2.line(crop_img, start, end, [0, 255, 0], 2)

    if count_defects == 2:
        print("Screen Shot")
    elif count_defects == 3:
        print("Picture")
        img_name = "picture_{}.png".format(img_counter)
        cv2.imwrite(img_name, picture)
        img_counter += 1

    cv2.imshow('mask', img)

    keypress = cv2.waitKey(1) & 0xFF
    if keypress == ord("s") or keypress == ord("q"):
        return False, img_counter

    return True, img_counter
