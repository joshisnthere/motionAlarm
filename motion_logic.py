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

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    significant = [c for c in contours if cv2.contourArea(c) > MIN_CONTOUR_AREA]

    return len(significant) > 0, significant
