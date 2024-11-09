import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import time

def start_detection():
    # Load the model directly without command-line arguments
    model_path = 'testmodel.tflite'
    camera_id = 0
    width, height = 640, 480
    num_threads = 4
    enable_edgetpu = False

    # Initialize the object detection model
    base_options = core.BaseOptions(
      file_name=model_path, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
      max_results=1, score_threshold=0.7)
    options = vision.ObjectDetectorOptions(
      base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # base_options = core.BaseOptions(file_name=model_path, use_coral=enable_edgetpu, num_threads=num_threads)
    # detection_options = processor.DetectionOptions(max_results=1, score_threshold=0.7)
    # options = vision.ObjectDetectorOptions(base_options=base_options, detection_options=detection_options)
    # detector = vision.ObjectDetector.create_from_options(options)

    # Start capturing video
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print('ERROR: Unable to read from webcam.')
            break

        # Flip and prepare the image for model inference
        image = cv2.flip(image, 1)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection
        detection_result = detector.detect(input_tensor)
        image = utils.visualize(image, detection_result)

        # Return the frame and detections
        yield image, detection_result

    cap.release()
    cv2.destroyAllWindows()
