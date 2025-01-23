import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load YOLO Model
def load_yolo_model(weights_path, config_path):
    # Load YOLO model and weights
    net = cv2.dnn.readNetFromDarknet(config_path, weights_path)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return net, output_layers

# Function to perform object detection
def detect_objects(frame, net, output_layers, conf_threshold=0.5):
    # Get frame dimensions
    (h, w) = frame.shape[:2]
    
    # Prepare image as a blob for object detection
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0,0,0), True, crop=False)
    
    # Set the input to the network
    net.setInput(blob)
    outs = net.forward(output_layers)
    
    boxes = []
    confidences = []
    class_ids = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                w = int(detection[2] * w)
                h = int(detection[3] * h)

                # Calculate the bounding box coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    return boxes, confidences, class_ids

# Draw bounding boxes on detected objects
def draw_boxes(frame, boxes, confidences, class_ids, labels, colors):
    for i in range(len(boxes)):
        x, y, w, h = boxes[i]
        confidence = confidences[i]

        label = f"{labels[class_ids[i]]}: {round(confidence * 100, 2)}%"
        color = colors[class_ids[i] % len(colors)]
        
        # Draw rectangle and label
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    return frame

# Load labels for object detection
def load_labels(labels_path='coco.names'):
    with open(labels_path, 'r') as f:
        labels = [line.strip() for line in f.readlines()]
    return labels

# Load YOLO model
weights_path = 'models/yolov3.weights'  # Path to YOLO weights file
config_path = 'models/yolov3.cfg'        # Path to YOLO config file

net, output_layers = load_yolo_model(weights_path, config_path)
labels = load_labels()
colors = np.random.uniform(0, 255, size=(len(labels), 3))

# Load input image
image_path = 'images/image1.jpg'  # Path to input image
image = cv2.imread(image_path)
image = cv2.resize(image, (800, 600))

# Perform object detection
boxes, confidences, class_ids = detect_objects(image, net, output_layers)

# Draw bounding boxes on the image
image_with_boxes = draw_boxes(image, boxes, confidences, class_ids, labels, colors)

# Convert image from BGR to RGB for displaying
image_with_boxes_rgb = cv2.cvtColor(image_with_boxes, cv2.COLOR_BGR2RGB)

# Display the result
plt.imshow(image_with_boxes_rgb)
plt.title("Detected Objects")
plt.show()

