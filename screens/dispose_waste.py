import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time
from tfprocess import detect  # Adjust path if needed

from utils.ir_util import is_object_close, sensor1, sensor2, sensor3
from utils.servo_util import move_servo
from utils.ultrasonic_util import get_distance, calculate_bin_level

class DisposeWaste(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)
        self.navigate_callback = navigate_callback

        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")

        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

        self.status_label = ctk.CTkLabel(self.left_frame, text="Scanning...", font=("Arial", 36), fg_color="white", bg_color="black")
        self.status_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.detection_label = ctk.CTkLabel(self.right_frame, text="", font=("Arial", 24), fg_color="black", bg_color="white")
        self.detection_label.pack(pady=20)

        # Bin level display, defaulted to 0%
        self.bin_labels = []
        for i in range(3):
            label = ctk.CTkLabel(self.right_frame, text=f"Bin {i+1} Level: 0%", font=("Arial", 16), fg_color="black", bg_color="white")
            label.pack()
            self.bin_labels.append(label)

        self.last_detection = None
        self.detection_start_time = None
        self.video_feed = None

    def success_detection(self):
        detection_type = self.last_detection
        sensors = {
            "Recyclable": (sensor1, 0),
            "Residual": (sensor2, 1),
            "Biodegradable": (sensor3, 2)
        }

        if detection_type in sensors:
            sensor, bin_index = sensors[detection_type]

            # Rotate the servo associated with the detected type
            move_servo(bin_index * 4, 180)
            time.sleep(0.5)

            # Check if object is close and update bin level
            if is_object_close(sensor):
                move_servo(bin_index * 4, 0)  # Reset servo to 0
                distance = get_distance(sensor)
                bin_level = calculate_bin_level(distance)
                self.bin_labels[bin_index].configure(text=f"Bin {bin_index+1} Level: {bin_level}%")
                print(f"{detection_type} detected: Bin {bin_index+1} Level: {bin_level}%")

    def detect_object(self):
        for frame, detection_result in detect.start_detection():
            self.update_camera_feed(frame)
            if detection_result.detections:
                label = detection_result.detections[0].categories[0].label
                self.detection_label.configure(text=label)

                # Trigger success detection if label matches last detection after 1 second
                if label == self.last_detection and time.time() - self.detection_start_time > 1:
                    self.success_detection()
                    break
                else:
                    self.last_detection = label
                    self.detection_start_time = time.time()
            else:
                self.detection_label.configure(text="No detection")
                self.last_detection = None
                self.detection_start_time = None

            self.update_idletasks()
            self.update()

    def update_camera_feed(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        if not self.video_feed:
            self.video_feed = tk.Label(self.left_frame)
            self.video_feed.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.video_feed.configure(image=imgtk)
        self.video_feed.image = imgtk

    def stop_detection(self):
        self.status_label.configure(text="Detection Stopped")
        self.detection_label.configure(text="Stopped")
