#!/bin/bash

if [ $# -eq 0 ]; then
  DATA_DIR="./"
else
  DATA_DIR="$1"
fi

# Install Python dependencies
python3 -m pip install pip --upgrade
python3 -m pip install -r requirements.txt

# Download TF Lite models
FILE=${DATA_DIR}/efficientdet_lite0.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/lite-model_efficientdet_lite0_detection_metadata_1.tflite' \
    -o ${FILE}
fi

FILE=${DATA_DIR}/efficientdet_lite0_edgetpu.tflite
if [ ! -f "$FILE" ]; then
  curl \
    -L 'https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/efficientdet_lite0_edgetpu_metadata.tflite' \
    -o ${FILE}
fi

# Copy testmodel.tflite to the target directory if not already there
FILE=${DATA_DIR}/garbage_classifier_model.tflite
if [ ! -f "$FILE" ]; then
  cp "/garbage_classifier_model.tflite" "${DATA_DIR}"
fi

echo -e "Downloaded files and testmodel.tflite are in ${DATA_DIR}"
