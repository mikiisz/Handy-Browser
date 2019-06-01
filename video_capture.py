from subprocess import Popen
from sys import executable

import cv2

arg1 = arg2 = arg3 = arg4 = 0


class MyVideoCapture:
    count = 0
    mod = 0
    card = 0
    data = []
    fingers = []
    x_prev = 0
    y_prev = 0
    # x_offset = 150
    # y_offset = 150
    start = False
    first = False
    driver = 0
    homePage = "http://www.google.com/"

    def __init__(self, video_source):
        # Open the video source
        self.cap = cv2.VideoCapture(video_source)
        self.backSub = cv2.createBackgroundSubtractorMOG2(history=500,
                                                          varThreshold=16,
                                                          detectShadows=True)
        if not self.cap.isOpened():
            raise ValueError("Unable to open video source", video_source)

    def get_frame(self, max_points, sensitivity, x_offset, y_offset):
        if self.cap.isOpened():
            ret, img = self.cap.read()
            img = cv2.flip(img, 1)
            fg_mask = self.backSub.apply(img)
            mask = img.copy()
            global arg1, arg2, arg3, arg4
            arg1 = max_points
            arg2 = sensitivity
            arg3 = x_offset
            arg4 = y_offset

            contours, tmp = cv2.findContours(fg_mask, cv2.RETR_LIST,
                                             cv2.CHAIN_APPROX_SIMPLE)

            size = i = 0
            # max_points = 100000
            # sensitivity = 5000

            x = y = w = h = 0
            x_average = y_average = 0

            for cnt in contours:
                i += 1
                if sensitivity < cv2.contourArea(cnt) and max_points > i:
                    (x, y, w, h) = cv2.boundingRect(cnt)
                    cv2.rectangle(mask, (x, y), (x + w, y + h), (255, 255, 0),
                                  0)
                    cv2.drawContours(fg_mask, [cnt], 0, (255, 255, 255), -1)
                    x_average += x + w / 2
                    y_average += y + h / 2
                    # print(x_average, y_average)
                    cv2.circle(mask, (int(x_average), int(y_average)), 5,
                               (0, 255, 0),
                               -1)
                    size += 1

            if size != 0:
                x_average = x_prev = int(x_average / size)
                y_average = y_prev = int(y_average / size)

            crop_img = fg_mask[
                       max(y_average - y_offset, 0):min(
                           y_average + y_offset,
                           480),
                       max(x_average - x_offset, 0):min(
                           x_average + x_offset,
                           640)
                       ]

            value = (35, 35)
            blurred = cv2.GaussianBlur(crop_img, value, 0)
            _, thresh = cv2.threshold(blurred, 127, 255,
                                      cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # cv2.imshow("fgMask", fgMask)
            # cv2.imshow("mask", img)
            # # cv2.imshow('crop_img', crop_img)
            # cv2.imshow("blurred", blurred)
            # cv2.imshow("thresh", thresh)
            # if contours:
            #     cv2.imshow("drawing", drawing)

            if ret:
                return ret, cv2.cvtColor(mask, cv2.COLOR_BGR2RGB), thresh
            else:
                return ret, None, None
        else:
            return None, None

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()


def start(pages, browser):
    # print(pages, browser)

    return [pages, browser, arg1, arg2, arg3, arg4]
    # Popen([executable, 'hand.py'])
    # hd.hand()
    # exec(open('hand.py').read())
