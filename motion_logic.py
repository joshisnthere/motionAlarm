"""
Frame-differencing motion detection. Compares two blurred grayscale frames,
thresholds the difference, and returns whether the total changed area is
big enough to count as "motion" along with the contours that triggered it.
"""

import cv2

MIN_CONTOUR_AREA = 900