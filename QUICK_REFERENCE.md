# ⚡ Quick Reference Guide

## 📁 File Structure Quick Look

```
IOMP/
├── app.py                    ← Main Flask Backend
├── requirements.txt          ← Install packages
├── README.md                 ← Full Documentation
├── SETUP.md                  ← Quick Setup
├── PROJECT_GUIDE.md          ← Detailed Guide (YOU ARE HERE)
├── QUICK_REFERENCE.md        ← This File
├── models/best.pt            ← Your YOLOv8 Model (PLACE HERE)
├── templates/index.html      ← Web Page
├── static/
│   ├── style.css            ← Styling
│   ├── script.js            ← JavaScript Logic
│   ├── uploads/             ← Uploaded Images
│   └── results/             ← Detection Results
```

---

## 🚀 Running the Project (3 Steps)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run backend
python app.py

# 3. Open browser
http://127.0.0.1:5000
```

---

## 📋 Dependencies

| Package | Version | Why |
|---------|---------|-----|
| flask | 3.0.0 | Web server |
| ultralytics | 8.1.10 | YOLOv8 |
| opencv-python | 4.8.1.78 | Image processing |
| numpy | 1.24.3 | Math operations |

---

## 🔌 API Endpoints

### GET `/`
Returns HTML page

### POST `/detect`
Upload image, get detection
```json
{
  "ambulance": true/false,
  "confidence": 0.87,
  "result_image": "/static/results/..."
}
```

### GET `/health`
Check if model is loaded
```json
{
  "status": "ok",
  "model_status": "loaded"
}
```

---

## 🎨 Frontend Files

### index.html
- Upload button
- Display images
- Show results
- Traffic lights

### style.css
- 1000+ lines of CSS
- Responsive design
- Traffic light animations
- Glow effects

### script.js
- File upload handling
- Image detection
- Traffic light control
- Debug functions

---

## ⚙️ App.py Key Sections

| Section | Line | Purpose |
|---------|------|---------|
| Imports | 1-10 | Libraries |
| Config | 17-28 | Folder setup |
| Model Load | 32-41 | YOLOv8 init |
| allowed_file() | 45-47 | Validate files |
| draw_bounding_boxes() | 55-92 | Draw detections |
| @app.route('/') | 95-98 | Home page |
| @app.route('/detect') | 101-175 | Detection |
| @app.route('/health') | 178-185 | Health check |
| app.run() | 188-200 | Start server |

---

## 🎯 Configuration Changes

### Change Confidence Threshold
**File**: app.py, Line 106
```python
conf=0.5  # Change this (0.3 to 0.95)
```

### Change Traffic Light Duration
**File**: script.js, Line 314
```javascript
}, 3000);  // Change milliseconds
```

### Change Port
**File**: app.py, Line 157
```python
port=5000  # Change this
```

### Change Upload Limit
**File**: app.py, Line 23
```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # Change size
```

---

## 🚦 Traffic Light States

| State | Duration | Color |
|-------|----------|-------|
| RED | 3s | 🔴 |
| GREEN | 3s | 🟢 |
| YELLOW | 3s | 🟡 |
| AMBULANCE | Active | 🚑 |

---

## 🐛 Quick Troubleshooting

| Error | Fix |
|-------|-----|
| Module not found | `pip install -r requirements.txt` |
| Model not found | Copy best.pt to models/ |
| Port in use | Change port in app.py line 157 |
| CSS not loading | Refresh browser (Ctrl+Shift+R) |
| Image not processing | Check format (PNG, JPG) |

---

## 💡 Useful Console Commands

```javascript
// In browser console (F12):
debugStatus()   // Show current state
debugReset()    // Reset application
```

---

## 📊 Expected Output

### Console (Terminal)
```
============================================================
Smart Traffic Control System
============================================================
Starting Flask server...
Open browser: http://127.0.0.1:5000
============================================================

Loading YOLOv8 model...
✓ Model loaded successfully!
```

### Browser Console (F12)
```
Smart Traffic Control System Started
✓ App initialized successfully
Backend Status: ok
Model Status: loaded
```

---

## 🎯 File Format Support

✅ PNG
✅ JPG
✅ JPEG
✅ GIF
✅ BMP

❌ WebP
❌ TIFF
❌ SVG

---

## 📈 Detection Workflow Summary

1. User uploads image
2. JavaScript reads file
3. Sends to `/detect` endpoint
4. Python processes with YOLOv8
5. OpenCV draws boxes
6. Saves result image
7. Returns JSON response
8. JavaScript updates UI
9. Traffic lights adjust

---

## 🔑 Key JavaScript Functions

```javascript
handleFileSelected()      // Process file upload
runDetection()           // Send to backend
updateDetectionResults() // Update UI
startNormalTrafficCycle()// Start lights
activateAmbulanceMode()  // Emergency mode
```

---

## 🔑 Key Python Functions

```python
allowed_file()          # Validate extensions
generate_filename()     # Create unique names
draw_bounding_boxes()   # Draw detections
@app.route('/detect')   # Detection endpoint
```

---

## 📝 File Sizes (Approximate)

| File | Size | Purpose |
|------|------|---------|
| app.py | 4KB | Backend |
| index.html | 8KB | Frontend |
| style.css | 12KB | Styling |
| script.js | 10KB | Logic |
| best.pt | 50-200MB | Model |

---

## ✅ Installation Verification

```bash
# Check Python
python --version

# Check pip
pip --version

# Check Flask
pip show flask

# Check ultralytics
pip show ultralytics

# Check OpenCV
pip show opencv-python

# Test imports
python -c "from ultralytics import YOLO; print('✓ Ready')"
```

---

## 🌐 Accessing Application

| URL | Purpose |
|-----|---------|
| http://127.0.0.1:5000 | Main interface |
| http://127.0.0.1:5000/health | Health check |
| http://127.0.0.1:5000/static/... | Static files |
| http://127.0.0.1:5000/detect | Detection API |

---

## 🎓 Learning Path

1. **Day 1**: Setup and run basic project
2. **Day 2**: Upload test images
3. **Day 3**: Customize settings
4. **Day 4**: Train own YOLOv8 model
5. **Day 5**: Deploy to production

---

## 🔗 External Resources

- [YOLOv8](https://docs.ultralytics.com/)
- [Flask](https://flask.palletsprojects.com/)
- [OpenCV](https://docs.opencv.org/)
- [Python](https://docs.python.org/)

---

## 📞 Getting Help

1. Check README.md
2. Check PROJECT_GUIDE.md
3. Check console output
4. Use debugStatus()
5. Check browser console (F12)

---

## ✨ Features at a Glance

✓ YOLOv8 ambulance detection
✓ Web-based interface
✓ Real-time processing
✓ Traffic light control
✓ Emergency mode
✓ Responsive design
✓ Easy customization
✓ Complete documentation

---

**Version**: 1.0.0
**Status**: ✅ Production Ready
**Last Updated**: February 27, 2026
