/* ========================================
   Smart Traffic Control System - JavaScript
   ======================================== */

// DOM Elements
const mediaInput = document.getElementById('mediaInput');
const detectBtn = document.getElementById('detectBtn');
const uploadedImageContainer = document.getElementById('uploadedImageContainer');
const processedImageContainer = document.getElementById('processedImageContainer');
const ambulanceStatus = document.getElementById('ambulanceStatus');
const confidenceScore = document.getElementById('confidenceScore');
const detectionMessage = document.getElementById('detectionMessage');
const loadingSpinner = document.getElementById('loadingSpinner');
const statusMessage = document.getElementById('statusMessage');
const fileInputLabel = document.querySelector('.file-input-label');

// Traffic Light Elements
const redLight = document.getElementById('redLight').querySelector('.light');
const yellowLight = document.getElementById('yellowLight').querySelector('.light');
const greenLight = document.getElementById('greenLight').querySelector('.light');
const ambulanceLight = document.getElementById('ambulanceLight').querySelector('.light');

// State Variables
let selectedFile = null;
let trafficLightInterval = null;
let isAmbulanceDetected = false;
let currentLightIndex = 0;

// Traffic Light Colors Array (for normal cycle)
const trafficLights = [redLight, greenLight, yellowLight];

/* ========================================
   FILE INPUT HANDLING
   ======================================== */

/**
 * Handle file selection from input
 */
mediaInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        handleFileSelected(file);
    }
});

/**
 * Handle drag and drop
 */
fileInputLabel.addEventListener('dragover', function(e) {
    e.preventDefault();
    fileInputLabel.classList.add('drag-over');
});

fileInputLabel.addEventListener('dragleave', function(e) {
    e.preventDefault();
    fileInputLabel.classList.remove('drag-over');
});

fileInputLabel.addEventListener('drop', function(e) {
    e.preventDefault();
    fileInputLabel.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        const file = files[0];
        if (file.type.startsWith('video/')) {
            handleFileSelected(file);
        } else {
            showStatusMessage('Please drop a video file', 'error');
        }
    }
});

/**
 * Handle file selection
 * @param {File} file - Selected file
 */
function handleFileSelected(file) {
    selectedFile = file;
    const dt = new DataTransfer();
    dt.items.add(file);
    mediaInput.files = dt.files;

    // Display selected media
    const url = URL.createObjectURL(file);
    displayMedia(url, file.type, uploadedImageContainer);
    showStatusMessage(`Video loaded: ${file.name}`, 'info');

    // Automatically run detection after uploading video
    runDetection();
}

/**
 * Display video in container
 * @param {string} src - Media source (data URL or path)
 * @param {string} type - MIME type
 * @param {HTMLElement} container - Container to display media
 */
function displayMedia(src, type, container) {
    container.innerHTML = '';

    const video = document.createElement('video');
    video.src = src;
    video.controls = true;
    video.loop = true;
    video.playsInline = true;
    video.style.maxWidth = '100%';
    video.style.height = 'auto';

    // Both uploaded and processed video: no autoplay, not muted
    if (container.id === "uploadedImageContainer" || container.id === "processedImageContainer") {
        video.autoplay = false;
        video.muted = false;
    }

    container.appendChild(video);
}

/* ========================================
   DETECTION HANDLING
   ======================================== */

/**
 * Handle detect button click
 */
detectBtn.addEventListener('click', async function() {
    if (!selectedFile) {
        showStatusMessage('Please select a video first', 'error');
        return;
    }

    await runDetection();
});

/**
 * Run YOLOv8 detection on selected video
 */
async function runDetection() {
    if (!selectedFile) {
        showStatusMessage('Please upload a video first', 'error');
        return;
    }

    try {
        detectBtn.disabled = true;
        loadingSpinner.classList.remove('hidden');
        statusMessage.classList.add('hidden');

        const formData = new FormData();
        formData.append('file', selectedFile);

        const response = await fetch('/detect_video', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        loadingSpinner.classList.add('hidden');
        detectBtn.disabled = false;

        if (result.success) {
            showStatusMessage(result.message, 'success');
            updateDetectionResults(result);
        } else {
            showStatusMessage(result.message || 'Detection failed', 'error');
            resetDetectionUI();
        }
    } catch (error) {
        console.error('Error:', error);
        loadingSpinner.classList.add('hidden');
        detectBtn.disabled = false;
        showStatusMessage(`Error: ${error.message}`, 'error');
        resetDetectionUI();
    }
}

/**
 * Update detection results in UI
 * @param {Object} result - Detection result from backend
 */
function getMediaTypeFromUrl(url) {
    if (!url) return 'image/jpeg';
    const ext = url.split('.').pop().toLowerCase();
    if (['mp4', 'webm', 'ogg', 'mkv', 'mov', 'avi'].includes(ext)) return 'video/' + (ext === 'mkv' ? 'x-matroska' : ext === 'mov' ? 'quicktime' : ext === 'avi' ? 'x-msvideo' : ext);
    if (['png', 'jpg', 'jpeg', 'gif', 'bmp'].includes(ext)) return 'image/' + (ext === 'jpg' ? 'jpeg' : ext);
    return 'image/jpeg';
}

function updateDetectionResults(result) {
    // Display uploaded media if available
    const uploadedMediaUrl = result.uploaded_video || result.uploaded_media;
    if (uploadedMediaUrl) {
        displayMedia(uploadedMediaUrl, getMediaTypeFromUrl(uploadedMediaUrl), uploadedImageContainer);
    } else {
        uploadedImageContainer.innerHTML = '<p class="placeholder">No uploaded media to display</p>';
    }

    // Display processed video
    let processedMediaUrl = result.result_video || result.processed_media;
    if (processedMediaUrl) {
        // Add cache-busting query string to force browser to reload the video
        const cacheBuster = Date.now();
        if (processedMediaUrl.indexOf('?') === -1) {
            processedMediaUrl += `?v=${cacheBuster}`;
        } else {
            processedMediaUrl += `&v=${cacheBuster}`;
        }
        displayMedia(processedMediaUrl, getMediaTypeFromUrl(processedMediaUrl), processedImageContainer);
    } else {
        processedImageContainer.innerHTML = '<p class="placeholder">No processed media to display</p>';
        // Fallback: show uploaded media also in processed section
        if (uploadedMediaUrl) {
            displayMedia(
                uploadedMediaUrl,
                getMediaTypeFromUrl(uploadedMediaUrl),
                processedImageContainer
            );
        }
    }
    // Debug: print backend response
    console.log("Backend response:", result);

    // Try to update dedicated result video element if present
    const resultVideo = document.getElementById("resultVideo");
    if (resultVideo) {
        if (result.result_video) {
            resultVideo.src = result.result_video + "?t=" + new Date().getTime();
            resultVideo.style.display = "block";
            resultVideo.load();
            resultVideo.play();
        } else {
            resultVideo.style.display = "none";
        }
    }

    // Update detection values
    isAmbulanceDetected = result.ambulance === true;
    ambulanceStatus.textContent = isAmbulanceDetected ? 'YES' : 'NO';
    ambulanceStatus.style.color = isAmbulanceDetected ? '#27ae60' : '#e74c3c';
    confidenceScore.textContent = result.confidence !== undefined ? (result.confidence * 100).toFixed(2) + '%' : '-';
    detectionMessage.textContent = result.message || 'Processed successfully';

    // Traffic control should reflect ambulance detection
    // If ambulance_frames is present, automate ambulance light indication
    if (result.ambulance_frames && Array.isArray(result.ambulance_frames) && result.ambulance_frames.length > 0) {
        // Show ambulance indication only for frames where ambulance detected
        let ambulanceFrameSet = new Set(result.ambulance_frames);
        // Animate ambulance light ON/OFF as video plays
        const resultVideo = document.getElementById("resultVideo");
        if (resultVideo) {
            resultVideo.addEventListener('timeupdate', function() {
                // Estimate current frame index
                const fps = resultVideo.fps || 20; // fallback fps
                const currentFrame = Math.floor(resultVideo.currentTime * fps);
                if (ambulanceFrameSet.has(currentFrame)) {
                    ambulanceLight.classList.add('active');
                } else {
                    ambulanceLight.classList.remove('active');
                }
            });
        }
    } else {
        ambulanceLight.classList.remove('active');
    }
    updateTrafficLights();
}

/**
 * Reset detection UI to initial state
 */
function resetDetectionUI() {
    ambulanceStatus.textContent = '-';
    ambulanceStatus.style.color = '#3498db';
    confidenceScore.textContent = '-';
    detectionMessage.textContent = '-';
    isAmbulanceDetected = false;
    updateTrafficLights();
}

/**
 * Show status message
 * @param {string} message - Message text
 * @param {string} type - Message type: 'success', 'error', 'info'
 */
function showStatusMessage(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusMessage.classList.add('hidden');
    }, 5000);
}

/* ========================================
   TRAFFIC LIGHT CONTROL
   ======================================== */

/**
 * Update traffic lights based on detection status
 */
function updateTrafficLights() {
    // Clear any existing intervals
    if (trafficLightInterval) {
        clearInterval(trafficLightInterval);
        trafficLightInterval = null;
    }

    // Reset all lights
    resetAllLights();

    if (isAmbulanceDetected) {
        // Emergency Mode: Activate ambulance light
        activateAmbulanceMode();
    } else {
        // Normal Mode: Start traffic light cycle
        startNormalTrafficCycle();
    }
}

/**
 * Activate all lights (for initialization)
 */
function resetAllLights() {
    redLight.classList.remove('active');
    yellowLight.classList.remove('active');
    greenLight.classList.remove('active');
    ambulanceLight.classList.remove('active');
}

/**
 * Activate ambulance emergency mode
 * All normal lights OFF, ambulance light ON with glow
 */
function activateAmbulanceMode() {
    resetAllLights();
    ambulanceLight.classList.add('active');
    console.log('🚑 AMBULANCE DETECTED - Emergency Mode Activated!');
}

/**
 * Start normal traffic light cycle
 * Cycles through: Red → Green → Yellow → Red...
 */
function startNormalTrafficCycle() {
    currentLightIndex = 0;

    // Immediately show first light
    updateCurrentLight();

    // Update light every 3 seconds
    trafficLightInterval = setInterval(() => {
        currentLightIndex = (currentLightIndex + 1) % trafficLights.length;
        updateCurrentLight();
    }, 3000);

    console.log('🚦 Normal Traffic Cycle Started');
}

/**
 * Update current active traffic light
 */
function updateCurrentLight() {
    resetAllLights();
    trafficLights[currentLightIndex].classList.add('active');

    // Update console for debugging
    const lightNames = ['RED', 'GREEN', 'YELLOW'];
    console.log(`Traffic Light: ${lightNames[currentLightIndex]}`);
}

/* ========================================
   INITIALIZATION
   ======================================== */

/**
 * Initialize the application
 */
function initializeApp() {
    console.log('========================================');
    console.log('Smart Traffic Control System Started');
    console.log('========================================');

    // Start initial traffic cycle
    startNormalTrafficCycle();

    // Check backend health
    checkBackendHealth();

    console.log('✓ App initialized successfully');
}

/**
 * Check backend health
 */
async function checkBackendHealth() {
    try {
        const response = await fetch('/health');
        const data = await response.json();
        console.log('Backend Status:', data.status);
        console.log('Model Status:', data.model_status);

        if (data.model_status === 'not_loaded') {
            showStatusMessage(
                'Warning: YOLOv8 model not loaded. Ensure models/best.pt exists.',
                'error'
            );
        }
    } catch (error) {
        console.warn('Could not connect to backend:', error);
    }
}

/* ========================================
   KEYBOARD SHORTCUTS
   ======================================== */

/**
 * Handle keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Spacebar to detect
    if (e.code === 'Space' && selectedFile && !detectBtn.disabled) {
        e.preventDefault();
        runDetection();
    }

    // R to reset
    if (e.code === 'KeyR') {
        resetUI();
    }
});

/**
 * Reset entire UI
 */
function resetUI() {
    selectedFile = null;
    mediaInput.value = '';
    uploadedImageContainer.innerHTML = '<p class="placeholder">No media uploaded yet</p>';
    processedImageContainer.innerHTML = '<p class="placeholder">Detection result will appear here</p>';
    resetDetectionUI();
    console.log('UI Reset');
}

/* ========================================
   RUN ON PAGE LOAD
   ======================================== */

document.addEventListener('DOMContentLoaded', initializeApp);

/* ========================================
   DEBUG UTILITIES (Remove in production)
   ======================================== */

// Window global functions for debugging
window.debugStatus = function() {
    console.log('=== DEBUG STATUS ===');
    console.log('Ambulance Detected:', isAmbulanceDetected);
    console.log('Selected File:', selectedFile ? selectedFile.name : 'None');
    console.log('Current Traffic Index:', currentLightIndex);
    console.log('Interval Active:', trafficLightInterval !== null);
};

window.debugReset = function() {
    console.log('Performing debug reset...');
    resetUI();
    startNormalTrafficCycle();
};

console.log('💡 Tip: Use debugStatus() and debugReset() in console for debugging');