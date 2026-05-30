# 📚 Smart Traffic Control System - Complete Project Guide

## ✅ Project Structure Verification

Your complete project structure is now ready:

```
IOMP/
│
├── 📄 app.py                              # Flask Backend (Main Application)
├── 📄 requirements.txt                    # Python Dependencies
├── 📄 README.md                           # Comprehensive Documentation
├── 📄 SETUP.md                            # Quick Setup Instructions
├── 📄 .gitignore                          # Git Ignore Rules
│
├── 📁 models/                             # YOLOv8 Model Storage
│   └── ➕ best.pt                         # (PLACE YOUR MODEL HERE)
│
├── 📁 static/                             # Frontend Static Files
│   ├── 📄 style.css                       # CSS Styling & Animations
│   ├── 📄 script.js                       # JavaScript Functionality
│   ├── 📁 uploads/                        # Uploaded Images
│   │   └── .gitkeep
│   └── 📁 results/                        # Detection Results
│       └── .gitkeep
│
└── 📁 templates/                          # HTML Templates
    └── 📄 index.html                      # Web Interface
```

---

## 🎯 Component Overview

### 1️⃣ Backend: app.py
**Purpose**: Flask server and YOLOv8 integration

**Key Functions**:
- Loads YOLOv8 model from `models/best.pt`
- Serves HTML interface via `/` route
- Handles image upload and detection via `/detect` route
- Processes images with OpenCV
- Returns JSON detection results

**Dependencies**:
```python
from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
import cv2
import os
from datetime import datetime
```

**Key Routes**:
- `GET /` - Render main page
- `POST /detect` - Process image and detect ambulance
- `GET /health` - Check backend status

---

### 2️⃣ Frontend: index.html
**Purpose**: Web user interface

**Sections**:
1. **Header** - Title and subtitle
2. **Left Panel** - Image upload, detection, results display
3. **Right Panel** - Traffic light control
4. **Footer** - Attribution

**Features**:
- Drag & drop file upload
- Real-time image preview
- Detection results display
- Traffic light visualization

---

### 3️⃣ Styling: style.css
**Purpose**: Visual design and animations

**Key Features**:
- Responsive design (mobile, tablet, desktop)
- Traffic light styling with glow effects
- Smooth animations and transitions
- Color scheme with CSS variables
- Dark and light mode ready

**CSS Variables**:
```css
--primary-color: #2c3e50
--secondary-color: #3498db
--success-color: #27ae60
--warning-color: #f39c12
--danger-color: #e74c3c
```

---

### 4️⃣ Logic: script.js
**Purpose**: Frontend interactivity

**Main Functions**:
- `handleFileSelected()` - Process uploaded image
- `runDetection()` - Send image to backend
- `updateDetectionResults()` - Update UI with results
- `startNormalTrafficCycle()` - Start traffic light cycle
- `activateAmbulanceMode()` - Activate emergency mode
- `debugStatus()` - Debug helper function

**Traffic Light Control**:
- Normal cycle: Red (3s) → Green (3s) → Yellow (3s)
- Emergency: All lights OFF → Ambulance light ON

---

## 🚀 Installation & Running

### Prerequisites Check
```powershell
# Check Python version
python --version          # Should be 3.8 or higher

# Check pip
pip --version             # Should be available
```

### Step-by-Step Installation

**Step 1: Prepare Model File**
```
1. Train/obtain best.pt (YOLOv8 model)
2. Copy to: C:\Users\ARCHANA\Downloads\IOMP\models\best.pt
```

**Step 2: Navigate to Project**
```powershell
cd C:\Users\ARCHANA\Downloads\IOMP
```

**Step 3: Install Dependencies**
```powershell
pip install -r requirements.txt
```

**Step 4: Start Application**
```powershell
python app.py
```

**Step 5: Open in Browser**
```
http://127.0.0.1:5000
```

---

## 📋 Requirements.txt Breakdown

| Package | Version | Purpose |
|---------|---------|---------|
| flask | 3.0.0 | Web framework for backend |
| ultralytics | 8.1.10 | YOLOv8 object detection |
| opencv-python | 4.8.1.78 | Image processing |
| numpy | 1.24.3 | Numerical operations |

---

## 🎨 Frontend Features Explained

### Upload Section
```
┌─────────────────────────────────┐
│  📸 Upload Image                │
│  ┌───────────────────────────┐  │
│  │ Drag image here or click  │  │
│  └───────────────────────────┘  │
│  [🔍 Detect Ambulance]          │
│  [Status Messages]              │
└─────────────────────────────────┘
```

### Image Display Section
```
┌──────────────┬──────────────┐
│   Uploaded   │  Processed   │
│    Image     │    Image     │
│   (Preview)  │  (Detection) │
└──────────────┴──────────────┘
```

### Detection Results
```
┌─────────────────────────────────┐
│ Ambulance Detected: ✓ YES       │
│ Confidence Score: 87.45%        │
│ Status: Ambulance detected!     │
└─────────────────────────────────┘
```

### Traffic Lights Section
```
┌──────────────────┐
│  🔴 RED          │  Normal cycle
│  🟢 GREEN        │  or
│  🟡 YELLOW       │  Emergency
│  🚑 AMBULANCE    │  mode
└──────────────────┘
```

---

## 🔄 Detection Workflow

```
User Uploads Image
        ↓
[index.html] displayImage()
        ↓
User Clicks Detect Button
        ↓
[script.js] runDetection()
        ↓
Fetch POST /detect
        ↓
[app.py] receive file
        ↓
Save to uploads/
        ↓
YOLOv8 Prediction
        ↓
Draw Bounding Boxes (OpenCV)
        ↓
Save to results/
        ↓
Return JSON Response
        ↓
[script.js] updateDetectionResults()
        ↓
Display Image & Confidence
        ↓
Update Traffic Lights
        ↓
Normal or Emergency Mode
```

---

## 🚦 Traffic Light Logic

### Normal Mode (No Ambulance)
```
Time: 0s    Light: 🔴 RED (STOP)
Time: 3s    Light: 🟢 GREEN (GO)
Time: 6s    Light: 🟡 YELLOW (CAUTION)
Time: 9s    Light: 🔴 RED (STOP) ← Cycle repeats
```

### Emergency Mode (Ambulance Detected)
```
Detection: ambulance_detected = true
Action: All lights OFF
Activate: 🚑 AMBULANCE light with glow effect
Priority: Give green light to ambulance direction
Recovery: Return to normal when ambulance no longer detected
```

---

## 💻 API Reference

### POST /detect

**Request:**
```
Content-Type: multipart/form-data
{
    "file": <image file>
}
```

**Response (Success):**
```json
{
    "success": true,
    "ambulance": true,
    "confidence": 0.8745,
    "uploaded_image": "/static/uploads/20260227_120530_photo.jpg",
    "result_image": "/static/results/result_20260227_120530_photo.jpg",
    "message": "Ambulance detected!"
}
```

**Response (No Ambulance):**
```json
{
    "success": true,
    "ambulance": false,
    "confidence": 0,
    "uploaded_image": "/static/uploads/20260227_120535_photo.jpg",
    "result_image": "/static/results/result_20260227_120535_photo.jpg",
    "message": "No ambulance detected"
}
```

**Response (Error):**
```json
{
    "success": false,
    "ambulance": false,
    "confidence": 0,
    "message": "File type not allowed"
}
```

---

## 🎯 Detection Parameters

**Confidence Threshold**: 0.5 (50%)
- Detections with confidence below 50% are filtered
- Adjust in app.py: `results = model.predict(image, conf=0.5)`

**Allowed Image Formats**: PNG, JPG, JPEG, GIF, BMP

**Max File Size**: 16MB

**Model Input**: Processed by YOLOv8 default preprocessing

---

## 🔧 Customization Guide

### 1. Change Confidence Threshold
**File**: [app.py](app.py#L106)
```python
# Line 106
results = model.predict(image, conf=0.5)  # Change to 0.3, 0.7, etc.
```

### 2. Change Traffic Light Timing
**File**: [script.js](static/script.js#L314)
```javascript
// Line 314
}, 3000);  // Change milliseconds (3000 = 3 seconds)
```

### 3. Change Port Number
**File**: [app.py](app.py#L157)
```python
# Line 157
app.run(debug=True, host='127.0.0.1', port=5000)  # Change port
```

### 4. Modify Colors
**File**: [style.css](static/style.css#L345)
```css
.red-light .light {
    background-color: #e74c3c;  /* Change hex color */
}
```

### 5. Change Page Title
**File**: [index.html](templates/index.html#L4)
```html
<title>Smart Traffic Control System</title>
```

---

## 📊 Model Validation

To validate your trained YOLOv8 model:

```bash
# Run validation
yolo task=detect mode=val model=models/best.pt data=data.yaml

# Interpret Results:
# Precision: TP / (TP + FP)  - Accuracy of positive predictions
# Recall: TP / (TP + FN)     - Coverage of actual positives
# mAP@0.5: Average precision at IoU=0.5
# mAP@0.5:0.95: Average precision across IoU thresholds
```

**Interpret Results**:
- **mAP > 0.90**: Excellent model
- **mAP 0.70-0.90**: Good model
- **mAP 0.50-0.70**: Acceptable model
- **mAP < 0.50**: Needs improvement

---

## 🐛 Common Issues & Solutions

### ❌ Model Not Found
```
Error: "Model file 'models/best.pt' not found"
✅ Solution: 
   1. Copy best.pt to models/ folder
   2. Verify file exists: ls models/best.pt
   3. Check file permissions
```

### ❌ Port Already in Use
```
Error: "Address already in use"
✅ Solution:
   1. Change port in app.py (line 157)
   2. Or kill existing process on port 5000
   PowerShell: lsof -ti:5000 | xargs kill -9
```

### ❌ Module Not Found
```
Error: "No module named 'ultralytics'"
✅ Solution:
   pip install --upgrade -r requirements.txt
```

### ❌ Image Not Processing
```
Error: Image upload fails or detection returns error
✅ Solution:
   1. Check image format (must be PNG, JPG, JPEG, GIF, BMP)
   2. Check file size (max 16MB)
   3. Check file permissions
   4. Verify model is loaded
```

### ❌ CSS/JavaScript Not Loading
```
Error: Page looks unstyled or buttons don't work
✅ Solution:
   1. Hard refresh browser (Ctrl+Shift+R)
   2. Clear browser cache (Ctrl+Shift+Delete)
   3. Try different browser
   4. Check console for 404 errors
```

---

## 🔒 Security Considerations

1. **File Upload Validation**
   - Only image formats allowed
   - File size limited to 16MB
   - Filename sanitization in place

2. **File Storage**
   - Uploaded files stored in designated folder
   - Results automatically indexed with timestamp
   - Old files can be manually cleaned

3. **For Production**
   - Change `debug=False` in app.py
   - Use production WSGI server (Gunicorn, uWSGI)
   - Add authentication/authorization
   - Use HTTPS instead of HTTP
   - Implement rate limiting
   - Add file cleanup scheduler

---

## 📈 Performance Tips

1. **Inference Speed**
   - Use GPU: Install `torch` with CUDA support
   - Reduce image resolution if needed
   - Lower confidence threshold cautiously

2. **Memory Usage**
   - Monitor with `top` or Task Manager
   - Close unnecessary applications
   - Consider lighter model variant if available

3. **Scaling**
   - Use threading enabled: `threaded=True` ✓
   - Consider load balancing for multiple users
   - Implement request queuing for high traffic

---

## 🚀 Deployment Options

### Local Development
```bash
python app.py
# Access: http://127.0.0.1:5000
```

### Production (Simple)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Advanced)
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

---

## 📞 Support & Debugging

### Console Debugging
Press `F12` in browser and use:
```javascript
// Check current status
debugStatus()

// Output: Shows ambulance detected, file selected, etc.

// Reset application
debugReset()

// Output: Resets UI and restarts traffic cycle
```

### Backend Debugging
In terminal, you'll see:
```
Loading YOLOv8 model...
✓ Model loaded successfully!
Traffic Light: RED
Traffic Light: GREEN
Traffic Light: YELLOW
...
```

### Check Backend Health
Navigate to: `http://127.0.0.1:5000/health`
Response:
```json
{
    "status": "ok",
    "model_status": "loaded"
}
```

---

## 📚 Additional Resources

- **YOLOv8 Docs**: https://docs.ultralytics.com/
- **Flask Docs**: https://flask.palletsprojects.com/
- **OpenCV Docs**: https://docs.opencv.org/
- **JavaScript Fetch**: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

---

## ✨ Features Summary

✅ **YOLOv8 Integration** - Real-time object detection
✅ **Web Interface** - Beautiful, responsive UI
✅ **Traffic Control** - Intelligent signal management
✅ **Emergency Mode** - Ambulance priority handling
✅ **Image Processing** - OpenCV bounding boxes
✅ **Drag & Drop** - Easy file upload
✅ **Responsive Design** - Works on desktop/tablet/mobile
✅ **Real-time Updates** - JavaScript without page reload
✅ **Error Handling** - Comprehensive validation
✅ **Documentation** - Complete setup and usage guide

---

## 🎉 You're All Set!

Your Smart Traffic Control System is ready to use!

**Next Steps:**
1. Place your `best.pt` model in `models/` folder
2. Run `pip install -r requirements.txt`
3. Execute `python app.py`
4. Open browser to `http://127.0.0.1:5000`
5. Upload test images and detect ambulances!

---

**Project Created**: February 27, 2026
**Version**: 1.0.0
**Status**: ✅ Ready for Development & Testing
