import cv2
from ultralytics import YOLO
import os

VIDEO_PATHS = [
    'videos/WhatsApp Video.mp4',
    'videos/Non Ambulance.mp4',
    'videos/Ambulance 1.mp4'
]

MODEL_PATH = 'models/best.pt'

def strict_ambulance_detection(results):
    ambulance_detected = False
    max_confidence = 0.0
    if results and len(results) > 0:
        result = results[0]
        if hasattr(result, 'boxes'):
            for box in result.boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"
                if 'ambulance' in class_name.lower() and confidence >= 0.7:
                    ambulance_detected = True
                    max_confidence = max(max_confidence, confidence)
    return ambulance_detected, max_confidence

def analyze_video(video_path, model):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Could not open video: {video_path}")
        return
    ambulance_frames = []
    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        results = model.predict(frame, conf=0.35, iou=0.35, max_det=3, verbose=False)
        detected, conf = strict_ambulance_detection(results)
        if detected:
            ambulance_frames.append(frame_idx)
        frame_idx += 1
    cap.release()
    print(f"\nVideo: {video_path}")
    print(f"Ambulance detected in {len(ambulance_frames)} frames.")
    print(f"Ambulance frame indices: {ambulance_frames}")

def main():
    if not os.path.exists(MODEL_PATH):
        print(f"Model not found at {MODEL_PATH}")
        return
    model = YOLO(MODEL_PATH)
    for video_path in VIDEO_PATHS:
        if os.path.exists(video_path):
            analyze_video(video_path, model)
        else:
            print(f"Video not found: {video_path}")

if __name__ == '__main__':
    main()