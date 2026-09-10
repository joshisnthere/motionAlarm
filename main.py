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

        os.makedirs(SNAPSHOT_DIR, exist_ok=True)

        self.video_label = ctk.CTkLabel(self, text="", fg_color=PANEL, corner_radius=12)
        self.video_label.pack(padx=20, pady=(20, 10))

        controls = ctk.CTkFrame(self, fg_color=PANEL, corner_radius=12)
        controls.pack(padx=20, pady=(0, 10), fill="x")
        ctk.CTkLabel(controls, text="Sensitivity", text_color=ACCENT).pack(side="left", padx=16, pady=14)
        self.sensitivity_slider = ctk.CTkSlider(controls, from_=1, to=50, number_of_steps=49)
        self.sensitivity_slider.set(15)
        self.sensitivity_slider.pack(side="left", fill="x", expand=True, padx=16)

        self.status_var = ctk.StringVar(value="Watching...")
        ctk.CTkLabel(self, textvariable=self.status_var, text_color="#8a8a8a").pack(anchor="w", padx=24)

        self.log_box = ctk.CTkTextbox(self, fg_color=PANEL, height=140, width=700)
        self.log_box.pack(padx=20, pady=(6, 20))
        self.log_box.configure(state="disabled")