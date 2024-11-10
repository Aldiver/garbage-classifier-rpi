import customtkinter as ctk
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import time
from tfprocess import detect  # Adjust path if needed

from utils.ir_util import get_sensor_value, sensor1, sensor2, sensor3
from utils.servo_util import move_servo
from utils.ultrasonic_util import get_distance, calculate_bin_level, ultrasonic_sensors

subcategories = {
        'Biodegradable': ['chopsticks', 'leaf', 'toothpick', 'Wooden Utensils', 'Juice Box', 'Paper Food Packages'],
        'Recyclable': ['cardboard', 'glass', 'metal', 'paper', 'plastic'],
        'Residual': ['bandaid', 'diapers', 'milkbox', 'napkin', 'pen', 'plasticene', 'rag', 'toothbrush', 'toothpastetube']
    }

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

        self.status_label = ctk.CTkLabel(self.left_frame, text="Scanning...", font=("Arial", 36), bg_color="black", fg_color="white")
        self.status_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.detection_label = ctk.CTkLabel(self.right_frame, text="n/a", font=("Arial", 24), fg_color="black", bg_color="white")
        self.detection_label.pack(pady=20)

        # Bin level display, defaulted to 0%
        self.bin_labels = []
        for i in range(3):
            label = ctk.CTkLabel(self.right_frame, text=f"Bin {i+1} Level: 0%", font=("Arial", 16), bg_color="black", fg_color="white")
            label.pack()
            self.bin_labels.append(label)

        self.last_detection = None
        self.detection_start_time = None
        self.video_feed = None

        self.update_bin_levels()

    def get_main_category(detection_type):
        # Loop through subcategories and find the main category
        for main_category, items in subcategories.items():
            if detection_type in items:
                return main_category
        return None  # Return None if no category is found

    def update_bin_levels(self):
    # Get the bin levels based on the distance readings from each ultrasonic sensor
        for i, sensor in enumerate(ultrasonic_sensors):  # Assuming `sensors` is the list of ultrasonic sensors
            distance = get_distance(sensor)  # Get distance from ultrasonic sensor
            bin_level = calculate_bin_level(distance)  # Calculate bin level based on distance

            # Update the bin level label in the GUI
            self.bin_labels[i].configure(text=f"Bin {i+1} Level: {bin_level}%")
            print(f"Bin {i+1} Level: {bin_level}% (Distance: {distance} cm)")


    def success_detection(self):
        detection_type = self.last_detection
        main_category = self.get_main_category(detection_type)
        sensors = {
            "Recyclable": (sensor1, 0, ultrasonic_sensors[0]),
            "Residual": (sensor2, 1, ultrasonic_sensors[1]),
            "Biodegradable": (sensor3, 2, ultrasonic_sensors[2])
        }
        print(f"Object detection category: {main_category}")
        if main_category:
            sensor, bin_index, ultrasonic_sensor = sensors[main_category]

            # Rotate the servo associated with the detected type
            print(f"Servo: {bin_index}")
            move_servo(bin_index * 4, 180)
            time.sleep(0.5)

            # Monitor the sensor for a 5-second allowance
            object_detected = False
            start_time = time.time()

            while time.time() - start_time < 5:
                if get_sensor_value(sensor) > 0.5:
                    object_detected = True
                    break
            time.sleep(0.1)  # Small delay to avoid tight loop

            # If object detected in the 5-second window
            if object_detected:
                move_servo(bin_index * 4, 0)  # Reset servo to 0
                distance = get_distance(ultrasonic_sensor)
                bin_level = calculate_bin_level(distance)
                self.bin_labels[bin_index].configure(text=f"Bin {bin_index+1} Level: {bin_level}%")
                print(f"{detection_type} detected: Bin {bin_index+1} Level: {bin_level}%")
                # TODO: Add points for successful disposal

            else:
                # If no object was detected, reset servo and navigate to home
                move_servo(bin_index * 4, 0)  # Reset servo to 0
                distance = get_distance(ultrasonic_sensor)
                bin_level = calculate_bin_level(distance)
                self.bin_labels[bin_index].configure(text=f"Bin {bin_index+1} Level: {bin_level}%")
                print(f"No trash inserted for {detection_type}. Returning to home screen.")
                # TODO: Display message and navigate to home screen

    def detect_object(self):
        for frame, detection_result in detect.start_detection():
            self.update_camera_feed(frame)
            if detection_result.detections:
                label = ""
                for detection in detection_result.detections:
                    for category in detection.categories:
                        label = category.category_name
                        confidence = category.score

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
