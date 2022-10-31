import logging as log
import random as rd
import time

import cv2 as cv
import numpy as np
import pyautogui as pag
import winsound as ws


def rand_pos(pos, left_bound=25, right_bound=25):
    left_bound = 0 - left_bound
    return pos + rd.randint(left_bound, right_bound)


def cv_match_temp(_img_bgr, template, threshold) -> bool:
    img_gray = cv.cvtColor(_img_bgr, cv.COLOR_BGR2GRAY)
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    _matched = False
    for pt in zip(*loc[::-1]):
        if pt is not None:
            _matched = True
            break

    return _matched


# logging module
log.basicConfig(level=log.INFO, format='[%(asctime)s.%(msecs)03d] %(message)s', datefmt='%Y/%m/%d, %H:%M:%S')

# click positions
DRAW_POS = (1321, 1007)
CONFIRM_POS = (1171, 752)
SKIP_POS = (1777, 53)
CLOSE_POS = (1842, 47)

# cv match threshold
THRESHOLD_SG_WISH_BTN = 0.95
THRESHOLD_CLS_BTN = 0.95

# read templates
TP_SG_WISH_BTN = cv.imread('resources\\temp_sg_wish_btn.jpg', 0)
TP_CLS_BTN = cv.imread('resources\\temp_cls_btn.jpg', 0)

# total draw times
TTL_DRAW = 1000
remaining_draw = TTL_DRAW

input('press enter to continue...\n')
time.sleep(5)
ws.Beep(500, 1500)

loop_times_outer = 0
while remaining_draw > 0:
    loop_times_outer += 1
    time.sleep(rd.uniform(0.05, 0.10))
    img_rgb = pag.screenshot()
    img_bgr = cv.cvtColor(np.asarray(img_rgb), cv.COLOR_RGB2BGR)
    matched = cv_match_temp(img_bgr, TP_SG_WISH_BTN, THRESHOLD_SG_WISH_BTN)

    if matched:
        pag.click(rand_pos(DRAW_POS[0], 50, 50),
                  rand_pos(DRAW_POS[1]))
        time.sleep(rd.uniform(0.15, 0.20))
        pag.click(rand_pos(CONFIRM_POS[0], 35, 35),
                  rand_pos(CONFIRM_POS[1]))
        remaining_draw -= 1
        log.info('Draw action complete. Current draw times: %d' % (TTL_DRAW - remaining_draw))
        time.sleep(rd.uniform(0.35, 0.40))

        loop_times = 0
        while True:
            loop_times += 1
            pag.click(
                rand_pos(SKIP_POS[0], 15, 10),
                rand_pos(SKIP_POS[1], 15, 10),
                clicks=2, interval=rd.uniform(0.03, 0.08))

            img_rgb = pag.screenshot()
            img_bgr = cv.cvtColor(np.asarray(img_rgb), cv.COLOR_RGB2BGR)
            matched = cv_match_temp(img_bgr, TP_CLS_BTN, THRESHOLD_CLS_BTN)
            matched2 = cv_match_temp(img_bgr, TP_SG_WISH_BTN, THRESHOLD_SG_WISH_BTN)
            # log.info(f'matched_close: {matched}')
            # log.info(f'matched_wish: {matched2}')

            if matched and (not matched2):
                # time.sleep(rd.uniform(0.30, 0.35))
                if loop_times > 1:
                    pag.click(rand_pos(CLOSE_POS[0], 20, 20),
                              rand_pos(CLOSE_POS[1], 20, 20),
                              clicks=2, interval=rd.uniform(0.02, 0.04))
                    log.info('Close action complete.')
                    break

            if loop_times > 5:
                log.warning('Failsafe Enabled!')
                break
