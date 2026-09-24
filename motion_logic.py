"""
Frame-differencing motion detection. Compares two blurred grayscale frames,
thresholds the difference, and returns whether the total changed area is
big enough to count as "motion" along with the contours that triggered it.
"""

import cv2

MIN_CONTOUR_AREA = 900


def detect_motion(prev_gray, current_gray, threshold):
    diff = cv2.absdiff(prev_gray, current_gray)
    _, thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)