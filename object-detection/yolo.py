import cv2
import torch
from ultralytics import YOLO
model = YOLO('yolov8n.pt')  
def detect_objects(video_source=0):
    cap = cv2.VideoCapture(video_source)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("No frame captured. Exiting...")
            break
        results = model(frame)
        for result in results:
            for bbox in result.boxes:
                x1, y1, x2, y2 = map(int, bbox.xyxy[0])
                conf = bbox.conf[0]
                class_id = int(bbox.cls[0])
                class_name = model.names[class_id]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{class_name} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('YOLO Object Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

detect_objects(video_source=0)
