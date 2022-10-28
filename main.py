import logging as lg
import random as rd
import time

import cv2 as cv
import numpy as np
import pyautogui as pag
import winsound as ws


def rand_pos(pos, left_bound=-25, right_bound=25):
    return pos + rd.randint(left_bound, right_bound)


def cv_match_temp(_img_rgb, template, threshold) -> bool:
    img_gray = cv.cvtColor(_img_rgb, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)

    # _, max_val, _, max_loc = cv.minMaxLoc(res)
    # top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(img_rgb, top_left, bottom_right, (0, 255, 0), 2)

    # _matched = False
    # for r in res:
    #     if r.any() >= threshold:
    #         _matched = True
    #         break

    # w, h = template.shape[::-1]
    loc = np.where(res >= threshold)
    _matched = False
    for pt in zip(*loc[::-1]):
    #     cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        if pt is not None:
            _matched = True

    return _matched


# logging module
lg.basicConfig(level=lg.INFO, format='[%(asctime)s]  %(message)s', datefmt='%m/%d/%Y_%H:%M:%S')

# click positions
DRAW_POS = (1321, 1007)
CONFIRM_POS = (1171, 752)
SKIP_POS = (1777, 53)
CLOSE_POS = (1842, 47)

# cv match threshold
THRESHOLD_1 = 0.90
THRESHOLD_2 = 0.95

# read templates
TP_SG_WISH = cv.imread('resources\\temp_sg_wish.jpg', 0)
# TP_CLS_BTN = cv.imread('resources\\temp_cls_btn.png', 0)
TP_CLS_BTN = cv.imread('resources\\temp_cls_btn2.jpg', 0)

# total draw times
ttl_draw = 3
ttl_draw_copy = ttl_draw

input('press enter to continue...\n')
time.sleep(5)
ws.Beep(350, 1500)
while ttl_draw > 0:
    time.sleep(0.05 + rd.uniform(0, 0.05))
    # pag.screenshot('resources\\screenshot_1.jpg')
    # img_rgb = cv.imread('resources\\screenshot_1.jpg', 0)
    img = pag.screenshot()  # pag is rgb
    img_rgb = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)
    matched = cv_match_temp(img_rgb, TP_SG_WISH, THRESHOLD_1)

    if matched:
        pag.click(rand_pos(DRAW_POS[0], -50, 50),
                  rand_pos(DRAW_POS[1]))
        time.sleep(rd.uniform(0.20, 0.25))
        pag.click(rand_pos(CONFIRM_POS[0], -35, 35),
                  rand_pos(CONFIRM_POS[1]))
        ttl_draw -= 1
        lg.info('Draw action complete. Current draw times: %d' % (ttl_draw_copy - ttl_draw))
        # ws.Beep(350, 100)
        # time.sleep(0.85 + rd.uniform(0, 0.20))

        while True:
            pag.click(
                rand_pos(SKIP_POS[0], -10, 5),
                rand_pos(SKIP_POS[1], -5, 5),
                clicks=2, interval=rd.uniform(0.03, 0.08))
            time.sleep(rd.uniform(0.05, 0.10))

            # pag.screenshot('resources\\screenshot_2.jpg')
            # img_rgb = cv.imread('resources\\screenshot_2.jpg', 0)
            img = pag.screenshot()  # pag is rgb
            img_rgb = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)
            matched = cv_match_temp(img_rgb, TP_CLS_BTN, THRESHOLD_2)

            if matched:
                time.sleep(rd.uniform(0.10, 0.15))
                pag.click(rand_pos(CLOSE_POS[0], -20, 20),
                          rand_pos(CLOSE_POS[1], -20, 20))
                lg.info('Close action complete.')
                # ws.Beep(650, 100)
                break
