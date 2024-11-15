import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time

import requests
from tfprocess import detect  # Adjust path if needed
import threading

from utils.ir_util import get_sensor_value, sensor1, sensor2, sensor3
from utils.servo_util import move_servo
from utils.ultrasonic_util import get_distance, calculate_bin_level, ultrasonic_sensors
from utils.utils import API_URL

subcategories = {
        'Biodegradable': ['chopsticks', 'leaf', 'toothpick', 'Wooden Utensils', 'Juice Box', 'Paper Food Packages'],
        'Recyclable': ['cardboard', 'glass', 'metal', 'paper', 'plastic'],
        'Residual': ['bandaid', 'diapers', 'milkbox', 'napkin', 'pen', 'plasticene', 'rag', 'toothbrush', 'toothpastetube']
    }

class DisposeWaste(ctk.CTkFrame):
    def __init__(self, parent, navigate_callback):
        super().__init__(parent)
        self.student = None

        self.navigate_callback = navigate_callback
        self.last_detection = None
        self.detection_start_time = None
        self.video_feed_initialized = False
        self.video_feed = None
        self.detection_active = False

        # Layout setup
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left and right frames
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=(10, 10), sticky="nsew")
        self.right_frame = ctk.CTkFrame(self, fg_color="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=(10, 10), sticky="nsew")

        # Status label
        self.status_label = ctk.CTkLabel(self.left_frame, text="Scanning...", font=("Arial", 36), bg_color="black", fg_color="white")
        self.status_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Detection label
        self.detection_label = ctk.CTkLabel(self.right_frame, text="n/a", font=("Arial", 24), fg_color="black", bg_color="white")
        self.detection_label.pack(pady=20)

        # Bin level display
        self.bin_labels = []
        for i in range(3):
            label = ctk.CTkLabel(self.right_frame, text=f"Bin {i+1} Level: 0%", font=("Arial", 16), bg_color="black", fg_color="white")
            label.pack()
            self.bin_labels.append(label)

        for label in self.bin_labels:
            label.pack()

        self.update_bin_levels()

    def get_main_category(self, detection_type):
        for main_category, items in subcategories.items():
            if detection_type in items:
                return main_category
        return None

    def update_bin_levels(self):
        for i, sensor in enumerate(ultrasonic_sensors):
            distance = get_distance(sensor)
            bin_level = calculate_bin_level(distance)
            self.bin_labels[i].configure(text=f"Bin {i+1} Level: {bin_level}%")
            print(f"Bin {i+1} Level: {bin_level}% (Distance: {distance} cm)")

    def start_detection(self):
        self.update()
        if not self.detection_active:
            self.detection_active = True
            threading.Thread(target=self.detect_object).start()
            # self.detect_object()

    def stop_detection(self):
        self.detection_active = False
        self.status_label.configure(text="Detection Stopped")
        self.detection_label.configure(text="Stopped")
        detect.stop_detection()  # Ensure detection process stops cleanly

    def success_detection(self):
        self.stop_detection()
        detection_type = self.last_detection
        self.last_detection = None
        main_category = self.get_main_category(detection_type)
        sensors = {
            "Recyclable": (sensor1, 0, ultrasonic_sensors[0]),
            "Residual": (sensor2, 1, ultrasonic_sensors[1]),
            "Biodegradable": (sensor3, 2, ultrasonic_sensors[2])
        }
        if main_category:
            sensor, bin_index, ultrasonic_sensor = sensors[main_category]
            print(f"Object detected: {detection_type} -> {main_category}")

            # Move servo and check for disposal
            move_servo(bin_index * 4, 180)
            time.sleep(0.5)
            object_detected = False
            start_time = time.time()

            while time.time() - start_time < 5:
                if get_sensor_value(sensor) > 0.5:
                    object_detected = True
                    break
                time.sleep(0.1)

            move_servo(bin_index * 4, 0)
            distance = get_distance(ultrasonic_sensor)
            bin_level = calculate_bin_level(distance)
            self.bin_labels[bin_index].configure(text=f"Bin {bin_index+1} Level: {bin_level}%")
            print(f"Bin {bin_index+1} Level: {bin_level}%")
            self.last_detection = None

            if object_detected:
                response = self.update_points()
                if response.status_code == 200:
                    self.show_success_modal(response)
                else:
                    message = self.get_error_message(response)
                    self.show_error_modal(message, retry_callback=self.update_points)

            else:
                self.show_success_modal("Failed to throw in correct bin, no points credited")

    def update_points(self):
        """
        Updates points by making a request to the server with the student's RFID.
        Returns the response or raises an exception if the request fails.
        """
        print(f"API fetch: {self.student_data}")
        url = f"{API_URL}/update-points/{self.student.rfid}"
        try:
            return requests.get(url)
        except requests.RequestException as e:
            # Handle request exceptions (e.g., network failure)
            self.show_error_modal(f"Error contacting server: {e}", retry_callback=self.update_points)
            return None  # return None if request failed

    def get_error_message(self, response):
        """
        Returns an appropriate error message based on the response status.
        """
        if response.status_code == 402:
            # Custom error message for 402
            data = response.json()
            return data.get('message', 'Student not found')
        else:
            # Default error message for other errors
            return f"Unexpected error: {response.status_code}"

    def detect_object(self):
        self.update()
        if not self.detection_active:
            return

        if not self.video_feed_initialized:
            print("Initializing video feed...")
            self.video_feed_initialized = True
            self.video_feed = tk.Label(self.left_frame)
            self.video_feed.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        while self.detection_active:
            for frame, detection_result in detect.start_detection():
                print("Detecting")
                if not self.detection_active:
                    break

                if detection_result.detections:
                    self.after(50, self.update_camera_feed, frame)
                    print("checking results")
                    for detection in detection_result.detections:
                        for category in detection.categories:
                            label = category.category_name
                            print(f"Checking category {label}")

                            if self.last_detection is None:
                                self.last_detection = label
                                self.detection_start_time = time.time()
                                print("Initialized last detection")
                            elif label == self.last_detection:
                                if (time.time() - self.detection_start_time) > 0.5:
                                    print("Successful detection confirmed")
                                    self.success_detection()
                                    break  # Exit after success
                            else:
                                # If the label differs, reset detection tracking
                                print("Detection mismatch, resetting timer")
                                self.last_detection = label
                                self.detection_start_time = time.time()

                    self.detection_label.configure(text=label)
                else:
                    print("No Detection Results")
                    self.detection_label.configure(text="No detection")
                    self.last_detection = None
                    self.detection_start_time = None

    def update_camera_feed(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_feed.configure(image=imgtk)
        self.video_feed.image = imgtk

    def update_with_student_data(self, student_data):
        self.student = student_data

    def show_success_modal(self, response):
        """
        Show a success modal with the response message and points.
        """
        data = response.json()
        message = data.get('message', 'Points updated successfully')
        current_points = data.get('current_points', 0)
        modal = ctk.CTkToplevel(self)
        modal.title("Success")
        modal.geometry("200x200")

        label = ctk.CTkLabel(modal, text=message, wraplength=180, justify="center")
        label.pack(pady=20)

        ok_button = ctk.CTkButton(modal, text="OK", command=lambda: [
            modal.destroy(),
            self.after(500, lambda: self.navigate_callback("main_menu"))
        ])
        ok_button.pack(pady=10)

    def show_error_modal(self, message, retry_callback=None):
        """
        Displays an error modal with options for retrying or navigating to the homepage.
        """
        modal = ctk.CTkToplevel(self)
        modal.title("Error")
        modal.geometry("200x200")

        label = ctk.CTkLabel(modal, text=message, wraplength=180, justify="center")
        label.pack(pady=20)

        button_frame = ctk.CTkFrame(modal)
        button_frame.pack(pady=10)

        # 'Try Again' button
        try_again_button = ctk.CTkButton(
            button_frame,
            text="Try Again",
            command=lambda: [modal.destroy(), retry_callback()]
        )
        try_again_button.grid(row=0, column=0, padx=5)

        # 'Go to Homepage' button
        homepage_button = ctk.CTkButton(
            button_frame,
            text="Go to Homepage",
            command=lambda: [modal.destroy(), self.navigate_callback("homepage")]
        )
        homepage_button.grid(row=0, column=1, padx=5)

        # Automatically navigate to Homepage after 5 seconds if no action is taken
        modal.after(10000, lambda: [modal.destroy(), self.navigate_callback("homepage")])
