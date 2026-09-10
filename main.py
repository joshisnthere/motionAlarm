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

import motion_logic as logic

ctk.set_appearance_mode("dark")

BG = "#100e0e"
PANEL = "#1c1918"
ACCENT = "#f2a154"
SNAPSHOT_DIR = os.path.join(os.path.dirname(__file__), "snapshots")


class MotionAlarmApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Webcam Motion Alarm")
        self.geometry("760x640")
        self.configure(fg_color=BG)