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

        self.cap = cv2.VideoCapture(0)
        self.prev_gray = None
        self.cooldown_until = None
        self._update_frame()

    def _update_frame(self):
        ok, frame = self.cap.read()
        if ok:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.prev_gray is not None:
                threshold = int(self.sensitivity_slider.get())
                triggered, contours = logic.detect_motion(self.prev_gray, gray, threshold)
                if triggered:
                    self._on_motion(frame, contours)
                    self.status_var.set("Motion detected")
                else:
                    self.status_var.set("Watching...")

            self.prev_gray = gray

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((720, 460))
            photo = ImageTk.PhotoImage(img)
            self.video_label.configure(image=photo)
            self.video_label.image = photo

        self.after(30, self._update_frame)

    def _on_motion(self, frame, contours):
        now = datetime.datetime.now()
        if self.cooldown_until and now < self.cooldown_until:
            return
        self.cooldown_until = now + datetime.timedelta(seconds=5)

        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (30, 165, 242), 2)

        filename = os.path.join(SNAPSHOT_DIR, now.strftime("%Y%m%d_%H%M%S.jpg"))
        cv2.imwrite(filename, frame)

        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{now.strftime('%H:%M:%S')}  motion detected -> {os.path.basename(filename)}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")