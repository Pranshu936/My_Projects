# YOLOv3 Object Detection with Webcam or Image Input

This project uses the YOLOv3 (You Only Look Once) object detection algorithm to detect objects in either a static image or real-time webcam feed. The YOLOv3 model is pre-trained to detect various objects such as people, cars, and animals, and it provides bounding boxes, class labels, and confidence scores for each detected object.

### Features:
- **Object Detection:** Detects multiple objects in real-time using webcam or from a static image.
- **Bounding Boxes:** Draws bounding boxes around detected objects with labels and confidence scores.
- **Real-time Webcam Detection:** Process and display live video feed with detected objects.
- **Static Image Detection:** Detect objects in a given image file and save the result.
- **Non-Maximum Suppression:** Reduces redundant bounding boxes using NMS (Non-Maximum Suppression) technique.

---

### Requirements:
To run the program, ensure you have the following dependencies installed:

- **Python 3.x**
- **Libraries**:
  - `opencv-python`: For video and image processing.
  - `numpy`: For numerical operations and array handling.

You can install the required libraries using `pip`:

```bash
pip install opencv-python numpy
```

Additionally, you'll need the following files:
- `yolov3.cfg`: The YOLOv3 configuration file.
- `yolov3.weights`: The YOLOv3 model weights file.
- `yolov3.txt`: A file containing the list of class labels the model can detect.

These files can be downloaded from the official YOLO website or other sources.

---

### How to Use:

1. **Run the Program:**
   - When you run the script, you will be prompted to choose between two modes:
     - **'image'**: Use an image file for detection.
     - **'webcam'**: Use your webcam for real-time object detection.

2. **For Image Input:**
   - After choosing the 'image' option, you will be asked to input the path to an image file.
   - The program will load the image, detect objects in it, display the processed image with bounding boxes, and save the result as `object-detection-output.jpg`.

3. **For Webcam Input:**
   - If you choose 'webcam', the program will start capturing frames from your webcam.
   - Detected objects will be displayed in real-time with bounding boxes, labels, and confidence scores.
   - Press `q` or `Esc` to stop the webcam stream and exit.

---

### How It Works:

1. **Model Loading:** 
   - The YOLOv3 model is loaded using the configuration and weights files. These files define the architecture and pre-trained weights for the model.

2. **Object Detection Process:**
   - The input image or webcam frame is passed through the YOLOv3 model to detect objects.
   - YOLO uses bounding box coordinates, class probabilities, and confidence scores to predict the objects.
   - Bounding boxes are drawn on detected objects, and labels with confidence scores are displayed.

3. **Non-Maximum Suppression (NMS):**
   - YOLO generates multiple bounding boxes for some objects, especially in crowded scenes. NMS is applied to remove redundant overlapping boxes.

4. **Visualization and Output:**
   - The detected objects are displayed on the screen, with bounding boxes, class names, and confidence scores.
   - For image input, the result is saved to a file (`object-detection-output.jpg`).

---

### File Paths:

Ensure the following files are correctly located in the specified paths (or modify the paths as per your directory structure):
- **Configuration File:** `yolov3.cfg`
- **Weights File:** `yolov3.weights`
- **Classes File:** `yolov3.txt`

---

### Customization:

- **Confidence Threshold:** You can adjust the `conf_threshold` variable to filter out weak detections. The default is set to `0.5`, meaning only detections with a confidence higher than 50% are considered.
- **Non-Maximum Suppression Threshold:** The `nms_threshold` controls the overlap allowed between boxes. Adjust it if needed to fine-tune the detection results.

---

### Troubleshooting:

- **Webcam Not Opening:** Ensure your webcam is correctly connected and accessible. Try using a different webcam ID (e.g., `cv2.VideoCapture(1)`) if the default doesn't work.
- **Image Not Loaded:** Make sure the image path is correct. The program will output an error if the image cannot be found.
- **Model Files Missing:** Ensure you have the YOLOv3 configuration, weights, and class labels files in the specified paths.

 ## YOLO (You Only Look Once)
 
 Download the pre-trained YOLO v3 weights file from this [link](https://pjreddie.com/media/files/yolov3.weights) and place it in the current directory or you can directly download to the current directory in terminal using
 
 `$ wget https://pjreddie.com/media/files/yolov3.weights`
 


