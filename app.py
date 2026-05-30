from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Real-time single-frame detection endpoint
@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    """Handle single frame (image) upload and run YOLOv8 detection"""
    try:
        if model is None:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Model not loaded. Please check models/best.pt"
            }), 500

        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No image uploaded"
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No selected file"
            }), 400

        # Read image as numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Invalid image data"
            }), 400

        # Run YOLOv8 detection
        results = model(img)
        ambulance_detected = False
        max_confidence = 0.0
        if results and len(results) > 0:
            result = results[0]
            if hasattr(result, 'boxes'):
                for box in result.boxes:
                    confidence = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"
                    if 'ambulance' in class_name.lower() and confidence > max_confidence:
                        max_confidence = confidence
                        ambulance_detected = True

        return jsonify({
            "success": True,
            "ambulance": ambulance_detected,
            "confidence": max_confidence,
            "message": "Ambulance detected in frame!" if ambulance_detected else "No ambulance detected in frame"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "ambulance": False,
            "confidence": 0,
            "message": f"Error: {str(e)}"
        }), 500
"""
Smart Traffic Control System with YOLOv8 Ambulance Detection
Uses Flask backend with YOLOv8 model for real-time ambulance detection
"""

from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
import time
from datetime import datetime
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
RESULT_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'mp4', 'mov', 'avi', 'mkv'}
MAX_FILE_SIZE = 120 * 1024 * 1024  # 120MB for video uploads

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Load YOLOv8 Model
print("Loading YOLOv8 model...")
try:
    model = YOLO("models/best.pt")
    print("✓ Model loaded successfully!")
except FileNotFoundError:
    print("✗ Error: Model file 'models/best.pt' not found!")
    print("Please ensure your trained YOLOv8 model (best.pt) is in the 'models' folder.")
except Exception as e:
    print(f"✗ Error loading model: {e}")
    model = None


def allowed_file(filename):
    """Check if file has allowed extension"""
    if '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


def generate_filename(original_filename):
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    return timestamp + original_filename


def draw_bounding_boxes(image, results, strict_ambulance_flag=False):
    """
    Draw bounding boxes and confidence scores on image
    
    Args:
        image: Input image (numpy array)
        results: YOLOv8 detection results
    
    Returns:
        image: Image with bounding boxes drawn
        ambulance_detected: Boolean indicating if ambulance was detected
        max_confidence: Highest confidence score
    """
    max_confidence = 0.0
    ambulance_detections = []  # Store all ambulance detections
    
    # Extract detections from results
    if results and len(results) > 0:
        result = results[0]
        
        # Get boxes and confidence scores
        if hasattr(result, 'boxes'):
            boxes = result.boxes
            
            for box in boxes:
                # Get coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # Get confidence
                confidence = float(box.conf[0])
                
                # Get class name
                class_id = int(box.cls[0])
                class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"

                # Track max confidence for display purposes
                if confidence > max_confidence:
                    max_confidence = confidence

                # Decide display label and color
                if 'ambulance' in class_name.lower():
                    # If strict ambulance detection flag is set, show as Ambulance; otherwise mark as Non Ambulance
                    display_label = 'Ambulance' if strict_ambulance_flag else 'Non Ambulance'
                    box_color = (0, 255, 0) if strict_ambulance_flag else (0, 0, 255)
                    ambulance_detections.append((confidence, x1, y1, x2, y2, class_name))
                else:
                    display_label = class_name
                    box_color = (255, 165, 0)  # Orange for other classes

                # Draw bounding box
                cv2.rectangle(image, (x1, y1), (x2, y2), box_color, 2)

                # Create label with display label and confidence
                label = f"{display_label}: {confidence:.2f}"
                
                # Get text size for background
                (text_width, text_height) = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                
                # Draw background rectangle behind text (same color as box)
                cv2.rectangle(image, (x1, y1 - text_height - 10), 
                            (x1 + text_width + 10, y1), box_color, -1)
                
                # Put text (class name and confidence)
                cv2.putText(image, label, (x1 + 5, y1 - 5), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
    
    return image, max_confidence


def draw_status_overlay(image, ambulance_detected, confidence):
    label = f"Ambulance: {'YES' if ambulance_detected else 'NO'} | Conf: {confidence:.2f}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = 0.8
    thickness = 2
    (text_w, text_h), _ = cv2.getTextSize(label, font, scale, thickness)
    x, y = 10, 30
    cv2.rectangle(image, (x - 5, y - text_h - 8), (x + text_w + 5, y + 5), (0, 0, 0), -1)
    cv2.putText(image, label, (x, y), font, scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return image


def strict_ambulance_detection(results):
    """
    Ambulance detection with configurable confidence threshold.
    Lowering threshold improves recall for partial/occluded ambulances.
    
    Returns: (ambulance_detected, confidence)
    """
    ambulance_detected = False
    max_confidence = 0.0
    ambulance_frame_time = None
    
    if results and len(results) > 0:
        result = results[0]
        
        if hasattr(result, 'boxes'):
            boxes = result.boxes
            
            for box in boxes:
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                class_name = result.names[class_id] if hasattr(result, 'names') else f"Class {class_id}"
                
                # Detect ambulance label with relaxed confidence threshold (0.80+)
                if 'ambulance' in class_name.lower() and confidence >= 0.80:
                    ambulance_detected = True
                    max_confidence = max(max_confidence, confidence)
    
    return ambulance_detected, max_confidence


def is_image_file(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in {'png', 'jpg', 'jpeg', 'gif', 'bmp'}


def is_video_file(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    return ext in {'mp4', 'mov', 'avi', 'mkv'}


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/detect', methods=['POST'])
def detect():
    """
    Handle image upload and run YOLOv8 detection
    
    Expected POST data:
        - file: Image file
    
    Returns:
        JSON with:
        {
            "success": true/false,
            "ambulance": true/false,
            "confidence": float,
            "uploaded_image": path to uploaded image,
            "result_image": path to processed image,
            "message": descriptive message
        }
    """
    
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Model not loaded. Please check models/best.pt"
            }), 500
        
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No file uploaded"
            }), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No file selected"
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Save uploaded image
        uploaded_filename = generate_filename(file.filename)
        uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
        file.save(uploaded_path)
        
        # Read image using OpenCV
        image = cv2.imread(uploaded_path)
        
        if image is None:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Could not read image file"
            }), 400
        
        # Run YOLOv8 detection with strict confidence threshold
        # Use conf=0.90 to get all potential detections, then apply ultra-strict logic
        results = model.predict(image, conf=0.90, iou=0.5)

        # Apply ULTRA-STRICT ambulance detection (requires 0.95+ confidence)
        # This empirically separates ambulances from false positives
        ambulance_detected, confidence = strict_ambulance_detection(results)

        # Draw bounding boxes and label image according to strict detection result
        # If strict detection is False, any 'ambulance' boxes are labeled 'Non Ambulance'
        processed_image, confidence_visual = draw_bounding_boxes(image, results, strict_ambulance_flag=ambulance_detected)

        # Use the ultra-strict detection confidence when available, otherwise fall back to visual max
        if not ambulance_detected:
            confidence = confidence_visual
        
        # Save processed image
        result_filename = "result_" + uploaded_filename
        result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
        cv2.imwrite(result_path, processed_image)
        
        # Return results as JSON
        return jsonify({
            "success": True,
            "ambulance": ambulance_detected,
            "confidence": round(confidence, 4),
            "uploaded_image": f"/{uploaded_path.replace(chr(92), '/')}",
            "result_image": f"/{result_path.replace(chr(92), '/')}",
            "message": "Ambulance detected!" if ambulance_detected else "No ambulance detected"
        }), 200
    
    except Exception as e:
        print(f"Error during detection: {str(e)}")
        return jsonify({
            "success": False,
            "ambulance": False,
            "confidence": 0,
            "message": f"Error: {str(e)}"
        }), 500


@app.route('/detect_video', methods=['POST'])
def detect_video():
    """Handle video upload and run YOLOv8 detection on video frames"""
    try:
        if model is None:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Model not loaded. Please check models/best.pt"
            }), 500

        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No video uploaded"
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "No file selected"
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400

        if not is_video_file(file.filename):
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Please upload a video file"
            }), 400

        uploaded_filename = generate_filename(file.filename)
        uploaded_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_filename)
        file.save(uploaded_path)

        cap = cv2.VideoCapture(uploaded_path)
        if not cap.isOpened():
            return jsonify({
                "success": False,
                "ambulance": False,
                "confidence": 0,
                "message": "Could not open uploaded video"
            }), 400

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        # Use a more browser-compatible codec (avc1/H264)
        try:
            fourcc = cv2.VideoWriter_fourcc(*'avc1')
        except:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # Build result video writer
        result_video_filename = "result_" + uploaded_filename
        result_video_path = os.path.join(app.config['RESULT_FOLDER'], result_video_filename)
        out = cv2.VideoWriter(result_video_path, fourcc, fps, (width, height))
        if not out.isOpened():
            out = None

        # Scale down for faster processing
        max_infer_width = 640
        if width > max_infer_width:
            scale = max_infer_width / float(width)
            infer_width = max_infer_width
            infer_height = int(height * scale)
        else:
            infer_width = width
            infer_height = height


        frame_skip = 5
        frame_idx = 0
        processed_frames = 0
        ambulance_detected = False
        max_confidence = 0.0
        ambulance_frames = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_has_ambulance = False
            frame_confidence = 0.0

            # ✅ MUST BE INSIDE LOOP
            if frame_idx % frame_skip == 0:
                frame_small = cv2.resize(frame, (256, int(frame.shape[0] * 256 / frame.shape[1])))

                results = model.predict(
                    frame_small,
                    conf=0.4,
                    iou=0.4,
                    imgsz=256,
                    verbose=False
                )

                frame_has_ambulance, frame_confidence = strict_ambulance_detection(results)

                if frame_has_ambulance:
                    ambulance_detected = True
                    ambulance_frames.append(frame_idx)
                    max_confidence = max(max_confidence, frame_confidence)

                processed_frame, _ = draw_bounding_boxes(
                    frame.copy(),
                    results,
                    strict_ambulance_flag=frame_has_ambulance
                )
            else:
                processed_frame = frame.copy()

            # ✅ ALWAYS WRITE FRAME
            if out is not None:
                out.write(processed_frame)

            processed_frames += 1
            frame_idx += 1

        # Close readers/writers
        cap.release()
        if out is not None:
            out.release()

        confidence = round(max_confidence, 4)
        message = "Ambulance detected in video!" if ambulance_detected else "No ambulance detected in video"
        static_uploaded_path = f"/static/uploads/{uploaded_filename}"
        static_result_path = f"/static/results/{result_video_filename}"

        return jsonify({
            "success": True,
            "ambulance": ambulance_detected,
            "confidence": confidence,
            "uploaded_video": static_uploaded_path,
            "result_video": static_result_path,
            "message": message,
            "processed_frames": processed_frames,
            "total_frames": frame_idx,
            "ambulance_frames": ambulance_frames
        }), 200

    except Exception as e:
        print(f"Error during video detection: {str(e)}")
        return jsonify({
            "success": False,
            "ambulance": False,
            "confidence": 0,
            "message": f"Error: {str(e)}"
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    model_status = "loaded" if model is not None else "not_loaded"
    return jsonify({
        "status": "ok",
        "model_status": model_status
    }), 200


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Smart Traffic Control System")
    print("="*60)
    print("Starting Flask server...")
    print("Open browser: http://127.0.0.1:5000")
    print("="*60 + "\n")
    
    # Run Flask app
    # debug=True enables auto-reload on code changes
    # threaded=True allows multiple requests simultaneously
    app.run(debug=True, host='127.0.0.1', port=5000, threaded=True)