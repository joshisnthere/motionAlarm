"""
Webcam Motion Alarm

Watches your webcam feed and flags motion above a sensitivity threshold you
control. When triggered it logs the event and saves a snapshot to
./snapshots -- a lightweight local security-cam substitute.
"""

import datetime
import os

import customtkinter as ctk
import cv2
from PIL import Image, ImageTk