# Smart Traffic Control System with YOLOv8 Ambulance Detection

A Flask-based web application that uses YOLOv8 for real-time ambulance detection and intelligent traffic light control.

## 🎯 Features

- **YOLOv8 Integration**: Real-time object detection using your trained ambulance detection model
- **Web Interface**: Beautiful, responsive UI built with Flask, HTML, CSS, and JavaScript
- **Traffic Light Control**: Intelligent traffic signal management with ambulance priority
- **Drag & Drop Upload**: Easy image upload with drag and drop support
- **Visual Feedback**: Bounding boxes with confidence scores on detected objects
- **Emergency Mode**: Automatic traffic light override when ambulance detected

## 📁 Project Structure

```
IOMP/
│
├── app.py                          # Flask backend (main application)
├── requirements.txt                # Python dependencies
│
├── models/
│   └── best.pt                     # YOLOv8 trained model (place your model here)
│
├── static/
│   ├── style.css                   # CSS styling
│   ├── script.js                   # JavaScript functionality
│   ├── uploads/                    # Uploaded images storage
│   └── results/                    # Processed detection results
│
└── templates/
    └── index.html                  # Web interface
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Your trained YOLOv8 model (best.pt)

### Step 1: Prepare Your Model

1. Place your trained YOLOv8 model file (`best.pt`) in the `models/` folder:
   ```
   IOMP/models/best.pt
   ```

### Step 2: Install Dependencies

Navigate to the project directory and install required packages:

```bash
cd c:\Users\ARCHANA\Downloads\IOMP
pip install -r requirements.txt
```

**Requirements:**
- Flask 3.0.0 - Web framework
- ultralytics 8.1.10 - YOLOv8 library
- opencv-python 4.8.1.78 - Computer vision
- numpy 1.24.3 - Numerical computing

### Step 3: Run the Application

```bash
python app.py
```

You should see:
```
============================================================
Smart Traffic Control System
============================================================
Starting Flask server...
Open browser: http://127.0.0.1:5000
============================================================
```

### Step 4: Open in Browser

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## 📖 How to Use

1. **Upload Image**
   - Click "Choose Image or Drag & Drop" button
   - Select an image or drag & drop an image file
   - Supported formats: PNG, JPG, JPEG, GIF, BMP

2. **Run Detection**
   - Click "🔍 Detect Ambulance" button
   - Wait for processing (image will show loading spinner)

3. **View Results**
   - Uploaded image displays on the left
   - Processed image with bounding boxes displays below
   - Detection results show confidence score

4. **Traffic Light Response**
   - **Normal Mode**: Traffic lights cycle Red → Green → Yellow (every 3 seconds)
   - **Emergency Mode**: When ambulance detected, all lights turn off and 🚑 Ambulance light activates with glow effect

## 🔧 Backend API

### Endpoints

#### GET `/` 
- **Description**: Render main web interface
- **Response**: HTML page

#### POST `/detect`
- **Description**: Upload image and run ambulance detection
- **Request**: 
  ```
  Form Data:
  - file: Image file (multipart/form-data)
  ```
- **Response**: 
  ```json
  {
    "success": true,
    "ambulance": true,
    "confidence": 0.8745,
    "uploaded_image": "/static/uploads/image.jpg",
    "result_image": "/static/results/result_image.jpg",
    "message": "Ambulance detected!"
  }
  ```

#### GET `/health`
- **Description**: Check backend and model status
- **Response**: 
  ```json
  {
    "status": "ok",
    "model_status": "loaded"
  }
  ```

## 🎨 Frontend Features

### Traffic Light States

| State | Lights | Behavior |
|-------|--------|----------|
| **Normal - Red** | 🔴 | Stop signal (3 seconds) |
| **Normal - Green** | 🟢 | Go signal (3 seconds) |
| **Normal - Yellow** | 🟡 | Caution signal (3 seconds) |
| **Emergency** | 🚑 | Ambulance detected, priority signal (glowing effect) |

### JavaScript Functions

#### `runDetection()`
- Sends image to backend for detection
- Handles response and updates UI

#### `updateTrafficLights()`
- Updates traffic light status based on detection
- Activates either normal cycle or emergency mode

#### `startNormalTrafficCycle()`
- Starts cyclical traffic light pattern
- Cycles every 3 seconds

#### `activateAmbulanceMode()`
- Activates emergency mode
- Turns on ambulance light with glow effect

### Debugging Console Commands

When you open browser developer console (F12), you can use:

```javascript
// Check current status
debugStatus()

// Reset application
debugReset()
```

## 📊 Model Validation & Accuracy

### Validate Your Model

To check your model's accuracy metrics:

```bash
yolo task=detect mode=val model=models/best.pt data=data.yaml
```

### Key Metrics

- **Precision**: Percentage of correct detections among all detections
- **Recall**: Percentage of actual objects that were detected
- **mAP@0.5**: Mean Average Precision at IoU threshold 0.5
- **mAP@0.5:0.95**: Mean Average Precision across IoU thresholds 0.5 to 0.95

### Model Configuration

The detection uses:
- **Confidence Threshold**: 0.5 (50%)
- **Model Path**: `models/best.pt`
- **Input**: Images up to 16MB

## 🛠️ Customization

### Change Confidence Threshold

Edit [app.py](app.py#L106):
```python
results = model.predict(image, conf=0.5)  # Change 0.5 to desired threshold
```

### Change Traffic Light Cycle Time

Edit [script.js](static/script.js#L320):
```javascript
}, 3000);  // Change 3000 to desired milliseconds
```

### Modify Traffic Light Colors

Edit [style.css](static/style.css#L345):
```css
.red-light .light {
    background-color: #e74c3c;  /* Modify color as needed */
}
```

## 🐛 Troubleshooting

### Error: "Model file 'models/best.pt' not found"
- **Solution**: Ensure your trained YOLOv8 model is placed in the `models/` folder
- **Check**: `c:\Users\ARCHANA\Downloads\IOMP\models\best.pt`

### Error: "No module named 'ultralytics'"
- **Solution**: Reinstall dependencies
  ```bash
  pip install --upgrade -r requirements.txt
  ```

### Port 5000 already in use
- **Solution**: Change port in [app.py](app.py#L157)
  ```python
  app.run(debug=True, host='127.0.0.1', port=5001)  # Use 5001 or another port
  ```

### Image not processing
- **Check**: 
  - Image format is supported (PNG, JPG, JPEG, GIF, BMP)
  - File size is less than 16MB
  - Model file is valid

### CSS/JavaScript not loading
- **Solution**: Clear browser cache (Ctrl+Shift+Delete)
- **Check**: Static files are in correct folders

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| **app.py** | Flask backend, model loading, detection endpoint |
| **requirements.txt** | Python package dependencies |
| **index.html** | Web UI structure and layout |
| **style.css** | Styling and animations |
| **script.js** | Image upload, detection, traffic light control |
| **best.pt** | YOLOv8 trained model (your file) |

## 🚦 How Traffic Control Works

### Normal Mode (No Ambulance)
```
Time 0-3s:   🔴 RED (STOP)
Time 3-6s:   🟢 GREEN (GO)
Time 6-9s:   🟡 YELLOW (CAUTION)
Time 9-12s:  🔴 RED (STOP) - cycle repeats
```

### Emergency Mode (Ambulance Detected)
```
Detection:   🔴🟢🟡 OFF → 🚑 AMBULANCE ON (glowing blue)
Priority:    All lane directions get GREEN for ambulance
Recovery:    Returns to normal cycle after image not detected
```

## 💡 Tips & Best Practices

1. **Model Training**: Ensure your YOLOv8 model is well-trained on ambulance images
2. **Image Quality**: Use clear, well-lit images for best detection
3. **Confidence Threshold**: Lower threshold catches more detections but may increase false positives
4. **Performance**: The app runs on CPU; GPU support available by modifying ultralytics installation
5. **Production**: Set `debug=False` in app.py for production deployment

## 📚 References

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenCV Documentation](https://docs.opencv.org/)

## 🔐 Security Notes

- Limit uploaded file size to prevent server overload
- Validate all file uploads (currently restricted to image types)
- Store uploaded images in designated folders
- Regular cleanup of old processed images recommended

## 📜 License

This project is provided as-is for educational and development purposes.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Review console output for error messages
3. Validate model file exists and is correct format
4. Check file permissions in IOMP folder

---

**Smart Traffic Control System v1.0**
Powered by YOLOv8 | Flask | OpenCV
