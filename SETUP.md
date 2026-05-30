# SETUP INSTRUCTIONS - Smart Traffic Control System

## ⚡ Quick Setup (30 seconds)

### 1. Place Your Model
```
Copy your best.pt file to: IOMP/models/best.pt
```

### 2. Install Dependencies
```powershell
cd C:\Users\ARCHANA\Downloads\IOMP
pip install -r requirements.txt
```

### 3. Run Application
```powershell
python app.py
```

### 4. Open Browser
```
http://127.0.0.1:5000
```

---

## 📦 What Gets Installed

```
flask==3.0.0                    # Web framework
ultralytics==8.1.10             # YOLOv8 library
opencv-python==4.8.1.78         # Computer vision
numpy==1.24.3                   # Numerical computing
```

---

## ✅ Verification Checklist

Before running, verify:

- [ ] Python 3.8+ installed (`python --version`)
- [ ] best.pt model placed in `models/` folder
- [ ] Running from IOMP directory
- [ ] Port 5000 is available
- [ ] Flask will start without errors

---

## 🐛 If Something Goes Wrong

### Issue: Module not found
```
Solution: pip install --upgrade -r requirements.txt
```

### Issue: Model not found
```
Solution: Verify models/best.pt exists
Check: ls models/ (should show best.pt)
```

### Issue: Port already in use
```
Solution: Edit app.py line 157 and change port number
Example: app.run(debug=True, host='127.0.0.1', port=5001)
```

---

## 📚 Next Steps

1. **Upload test images** to verify detection works
2. **Check model accuracy** using validation commands
3. **Customize traffic light timing** if needed
4. **Deploy to production** (set debug=False)

---

## 🔗 Key Files Reference

- **Backend**: `app.py`
- **Frontend**: `templates/index.html`
- **Styling**: `static/style.css`
- **Logic**: `static/script.js`
- **Model**: `models/best.pt`

---

Created: February 27, 2026
Version: 1.0
