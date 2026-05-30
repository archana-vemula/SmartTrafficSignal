from ultralytics import YOLO
import cv2
import numpy as np

model = YOLO('models/best.pt')

print("=" * 60)
print("Model Analysis")
print("=" * 60)
print(f"Classes in model: {model.names}")
print(f"Number of classes: {len(model.names)}")
print()

# Create a simple test image (solid color - non-ambulance)
test_image = np.zeros((640, 480, 3), dtype=np.uint8)
test_image[:] = (100, 100, 100)  # Grey background

print("Testing with grey image (should have NO ambulance)...")
results = model.predict(test_image, conf=0.3, verbose=False)

if results and len(results) > 0:
    result = results[0]
    print(f"Number of detections: {len(result.boxes)}")
    
    for i, box in enumerate(result.boxes):
        confidence = float(box.conf[0])
        class_id = int(box.cls[0])
        class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"
        print(f"  Detection {i+1}: {class_name} - Confidence: {confidence:.4f}")
        
        if 'ambulance' in class_name.lower():
            print(f"    ^^^ FALSE POSITIVE! Non-ambulance detected as ambulance!")
else:
    print("✓ Correct: No detections in grey image")