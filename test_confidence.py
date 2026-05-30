from ultralytics import YOLO
import cv2

model = YOLO('models/best.pt')

images_to_test = [
    'static/uploads/20260227_174417_ambulance.jpg',
    'static/uploads/20260227_174617_car2.jpg',
    'static/uploads/20260227_175101_car2.jpg'
]

print("=" * 70)
print("Testing Model Predictions on Real Images")
print("=" * 70)

for img_path in images_to_test:
    try:
        image = cv2.imread(img_path)
        if image is None:
            print(f"\n❌ Could not read: {img_path}")
            continue
            
        print(f"\n📷 Testing: {img_path}")
        
        # Test with different confidence thresholds
        for conf_threshold in [0.3, 0.5, 0.7, 0.85]:
            results = model.predict(image, conf=conf_threshold, verbose=False)
            
            if results and len(results) > 0 and hasattr(results[0], 'boxes'):
                boxes = results[0].boxes
                print(f"  conf={conf_threshold}: {len(boxes)} detections")
                for box in boxes:
                    confidence = float(box.conf[0])
                    print(f"    - ambulance: {confidence:.4f}")
            else:
                print(f"  conf={conf_threshold}: 0 detections")
                
    except Exception as e:
        print(f"Error with {img_path}: {e}")

print("\n" + "=" * 70)