import os
from ultralytics import YOLO
import cv2

# configuration
UPLOAD_DIR = 'static/uploads'
model = YOLO('models/best.pt')

# thresholds
prediction_conf_threshold = 0.90  # detection threshold used earlier in app
ambulance_conf_score = 0.95  # strict threshold in app

# gather files
total = 0
correct = 0

print("Evaluating model accuracy based on upload directory labels...")
print(f"Using prediction_conf_threshold={prediction_conf_threshold}, ambulance_conf_score={ambulance_conf_score}")
print()

for fname in os.listdir(UPLOAD_DIR):
    if fname.startswith('.'):
        continue
    total += 1
    path = os.path.join(UPLOAD_DIR, fname)
    truth = 'ambulance' if 'ambulance' in fname.lower() else 'car'

    img = cv2.imread(path)
    if img is None:
        print(f"Could not read {fname}")
        continue
    
    results = model.predict(img, conf=prediction_conf_threshold, verbose=False)
    detected = False
    best_conf = 0.0
    if results and len(results) > 0 and hasattr(results[0],'boxes'):
        for box in results[0].boxes:
            conf = float(box.conf[0])
            if 'ambulance' in results[0].names[int(box.cls[0])].lower():
                best_conf = max(best_conf, conf)
                if conf >= ambulance_conf_score:
                    detected = True
    
    pred_label = 'ambulance' if detected else 'car'
    ok = pred_label == truth
    if ok:
        correct += 1
    print(f"{fname}: truth={truth}, pred={pred_label}, conf={best_conf:.4f}, {'OK' if ok else 'WRONG'}")

print()
print(f"Total: {total}, Correct: {correct}, Accuracy: {correct/total*100:.2f}%")