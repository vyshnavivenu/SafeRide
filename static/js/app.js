/**
 * SafeRide Interactive Frontend Logic & SOS Dispatcher
 */

// Automatically refresh page if navigated via browser Back/Forward cache (prevents stale CSRF tokens)
window.addEventListener('pageshow', function (event) {
  if (event.persisted) {
    window.location.reload();
  }
});

// Helper to read CSRF token from document cookies or hidden inputs
function getCSRFToken() {
  const metaOrInput = document.querySelector('[name=csrfmiddlewaretoken]');
  if (metaOrInput && metaOrInput.value) {
    return metaOrInput.value;
  }
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue || '';
}

// Play Synthetic Web Audio Alert Beep for SOS dispatch
function playSOSAudioBeep() {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(880, audioCtx.currentTime); // A5 note
    osc.frequency.exponentialRampToValueAtTime(440, audioCtx.currentTime + 0.3);
    
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
    
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.start();
    osc.stop(audioCtx.currentTime + 0.6);
  } catch (e) {
    console.log("Web Audio API disabled or blocked:", e);
  }
}

// Universal Mobile Geolocation Helper with High-Accuracy -> Low-Accuracy Fallback Cascade
function getAccurateUserLocation(onSuccess, onError, customOptions = {}) {
  if (!("geolocation" in navigator)) {
    if (onError) onError({ code: -1, message: "Geolocation is not supported by your browser." });
    return;
  }

  const highAccuracyOptions = {
    enableHighAccuracy: true,
    timeout: 8000,
    maximumAge: 0,
    ...customOptions
  };

  const lowAccuracyOptions = {
    enableHighAccuracy: false,
    timeout: 12000,
    maximumAge: 60000,
    ...customOptions
  };

  // Step 1: Attempt High-Accuracy GPS
  navigator.geolocation.getCurrentPosition(
    (position) => {
      onSuccess(position.coords.latitude, position.coords.longitude, position.coords.accuracy || 10);
    },
    (firstError) => {
      console.warn("High-accuracy GPS timed out or unavailable. Falling back to cell/WiFi triangulation...", firstError);

      // If user explicitly denied permission, do not retry
      if (firstError.code === firstError.PERMISSION_DENIED) {
        if (onError) {
          onError({
            code: firstError.code,
            message: "⚠️ Location permission denied. Please allow location access in your browser or phone Settings to transmit live GPS coordinates."
          });
        }
        return;
      }

      // Step 2: Low-Accuracy Fallback (WiFi / Cellular tower positioning)
      navigator.geolocation.getCurrentPosition(
        (fallbackPosition) => {
          onSuccess(fallbackPosition.coords.latitude, fallbackPosition.coords.longitude, fallbackPosition.coords.accuracy || 50);
        },
        (finalError) => {
          console.warn("Low-accuracy geolocation fallback also failed:", finalError);
          let userMsg = "Location acquisition failed. Defaulting to transit coordinates.";
          if (finalError.code === finalError.PERMISSION_DENIED) {
            userMsg = "⚠️ Location access is blocked. Please enable Location Services in your phone Settings.";
          } else if (finalError.code === finalError.POSITION_UNAVAILABLE) {
            userMsg = "⚠️ GPS location signal unavailable on this device.";
          } else if (finalError.code === finalError.TIMEOUT) {
            userMsg = "⚠️ GPS location request timed out.";
          }
          if (onError) onError({ code: finalError.code, message: userMsg });
        },
        lowAccuracyOptions
      );
    },
    highAccuracyOptions
  );
}

// 1-Touch SOS Emergency Alert Trigger
function triggerSOSEmergency(tripId = null) {
  const btn = document.getElementById('global-confirm-sos-btn') || document.getElementById('confirm-sos-btn');
  const statusDiv = document.getElementById('global-sos-status-message') || document.getElementById('sos-status-message');
  
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Broadcasting Distress Beacon...';
  }

  playSOSAudioBeep();

  // Default campus/transit coordinate fallback
  let defaultLat = 9.6843; // Near Palai, Kerala
  let defaultLng = 76.6853;

  function sendSOSPayload(currentLat, currentLng) {
    const payload = {
      latitude: currentLat,
      longitude: currentLng,
      trip_id: tripId,
      location_name: "Live GPS Emergency Distress Signal"
    };

    fetch('/api/sos/trigger/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
      },
      body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        playSOSAudioBeep();
        if (statusDiv) {
          statusDiv.innerHTML = `
            <div class="alert alert-danger p-3 mb-0">
              <h5 class="fw-bold mb-1">🚨 EMERGENCY SOS BROADCAST ACTIVE</h5>
              <p class="small mb-2">Distress Beacon dispatched to Central Control Center & Police (112).</p>
              <div class="p-2 bg-white rounded text-dark small">
                <strong>Alert ID:</strong> #${data.alert_id.substring(0, 8)}<br>
                <strong>Timestamp:</strong> ${data.timestamp}<br>
                <strong>GPS Coordinates:</strong> ${currentLat.toFixed(4)}, ${currentLng.toFixed(4)}
              </div>
              <div class="mt-3">
                <a href="tel:112" class="btn btn-dark btn-sm w-100 fw-bold"><i class="fa-solid fa-phone me-1"></i> Call Police Control (112)</a>
              </div>
            </div>
          `;
        }
      } else {
        alert("Failed to broadcast SOS alert. Please call 112 directly.");
      }
    })
    .catch(err => {
      console.error("SOS Trigger Error:", err);
      alert("Error reaching emergency servers. Please dial 112 directly.");
    });
  }

  // Obtain accurate coordinates with high-to-low accuracy cascade
  getAccurateUserLocation(
    (userLat, userLng) => {
      sendSOSPayload(userLat, userLng);
    },
    (errObj) => {
      console.warn("GPS fallback applied:", errObj.message);
      if (statusDiv && errObj.code === 1) {
        statusDiv.innerHTML = `<div class="alert alert-warning p-2 small mb-2">${errObj.message}</div>`;
      }
      sendSOSPayload(defaultLat, defaultLng);
    }
  );
}

// ==========================================
// SAFERIDE SNAPSHOT-ONLY QR CODE SCANNER ENGINE
// ==========================================

let isSnapshotProcessing = false;

// Initialize QR modal listeners on page load
document.addEventListener("DOMContentLoaded", function () {
  const qrModalEl = document.getElementById('qrScannerModal');
  if (qrModalEl) {
    qrModalEl.addEventListener('shown.bs.modal', function () {
      resetSnapshotScanner();
    });
    qrModalEl.addEventListener('hidden.bs.modal', function () {
      resetSnapshotScanner();
    });
  }
});

/**
 * Triggers the native camera photo capture or file upload dialog.
 */
function triggerSnapshotCapture() {
  const fileInput = document.getElementById('qr-file-input');
  if (fileInput) {
    fileInput.click();
  }
}

/**
 * Resets the snapshot modal view to initial idle state.
 */
function resetSnapshotScanner() {
  isSnapshotProcessing = false;
  
  const idleView = document.getElementById('snapshot-idle-view');
  const previewView = document.getElementById('snapshot-preview-view');
  const previewImg = document.getElementById('snapshot-preview-img');
  const fileInput = document.getElementById('qr-file-input');
  const resultsDiv = document.getElementById('qr-reader-results');
  const retakeWrapper = document.getElementById('snapshot-retake-wrapper');
  const laserBeam = document.getElementById('snapshot-laser');

  if (idleView) idleView.classList.remove('d-none');
  if (previewView) previewView.classList.add('d-none');
  if (previewImg) previewImg.src = '';
  if (fileInput) fileInput.value = '';
  if (laserBeam) laserBeam.style.display = 'block';
  if (retakeWrapper) retakeWrapper.classList.add('d-none');

  if (resultsDiv) {
    resultsDiv.innerHTML = '<span class="text-white opacity-75"><i class="fa-solid fa-circle-info me-1 text-warning"></i> Ready. Tap the box above to snap the driver\'s QR badge.</span>';
  }
}

/**
 * Crops the image tightly around the detected QR code bounding box with focus framing.
 */
function cropAndFocusQRCode(sourceCanvas, bbox) {
  try {
    if (!sourceCanvas || !bbox || bbox.width <= 0 || bbox.height <= 0) return null;
    
    // Add 16% padding margin around QR code to include quiet zone
    const padX = bbox.width * 0.16;
    const padY = bbox.height * 0.16;
    
    const cropX = Math.max(0, bbox.x - padX);
    const cropY = Math.max(0, bbox.y - padY);
    const cropW = Math.min(sourceCanvas.width - cropX, bbox.width + padX * 2);
    const cropH = Math.min(sourceCanvas.height - cropY, bbox.height + padY * 2);
    
    const cropCanvas = document.createElement('canvas');
    cropCanvas.width = cropW;
    cropCanvas.height = cropH;
    const cropCtx = cropCanvas.getContext('2d');
    
    // Draw cropped QR code region
    cropCtx.drawImage(sourceCanvas, cropX, cropY, cropW, cropH, 0, 0, cropW, cropH);
    
    // Draw high-tech amber reticle brackets on the corners
    const bracketSize = Math.max(14, Math.min(cropW, cropH) * 0.12);
    const offset = Math.max(4, Math.min(cropW, cropH) * 0.03);
    cropCtx.strokeStyle = '#FF9800';
    cropCtx.lineWidth = Math.max(3, Math.min(cropW, cropH) * 0.025);
    cropCtx.lineCap = 'round';
    
    // Top-Left
    cropCtx.beginPath();
    cropCtx.moveTo(offset, offset + bracketSize);
    cropCtx.lineTo(offset, offset);
    cropCtx.lineTo(offset + bracketSize, offset);
    cropCtx.stroke();
    
    // Top-Right
    cropCtx.beginPath();
    cropCtx.moveTo(cropW - offset - bracketSize, offset);
    cropCtx.lineTo(cropW - offset, offset);
    cropCtx.lineTo(cropW - offset, offset + bracketSize);
    cropCtx.stroke();
    
    // Bottom-Left
    cropCtx.beginPath();
    cropCtx.moveTo(offset, cropH - offset - bracketSize);
    cropCtx.lineTo(offset, cropH - offset);
    cropCtx.lineTo(offset + bracketSize, cropH - offset);
    cropCtx.stroke();
    
    // Bottom-Right
    cropCtx.beginPath();
    cropCtx.moveTo(cropW - offset - bracketSize, cropH - offset);
    cropCtx.lineTo(cropW - offset, cropH - offset);
    cropCtx.lineTo(cropW - offset, cropH - offset - bracketSize);
    cropCtx.stroke();
    
    return cropCanvas.toDataURL('image/jpeg', 0.95);
  } catch (err) {
    console.warn("Auto-crop QR error:", err);
    return null;
  }
}

/**
 * Multi-pass high-precision Photo Snapshot Scanner with Auto-Crop & Focus:
 * Pass 1: jsQR (full canvas) + Auto-Crop
 * Pass 2: BarcodeDetector API (full canvas) + Auto-Crop
 * Pass 3: Center Zoom 60% Crop Pass (for small/distant QR codes)
 * Pass 4: Html5Qrcode ZXing engine static scan
 * Pass 5: Grayscale + High-Contrast Binarization Filter + Auto-Crop
 */
async function handleQRImageFile(input) {
  if (!input.files || input.files.length === 0) return;
  const file = input.files[0];
  
  // Automatically open modal if not already visible to display scanning progress & feedback
  const qrModalEl = document.getElementById('qrScannerModal');
  if (qrModalEl && typeof bootstrap !== 'undefined') {
    const modalInstance = bootstrap.Modal.getOrCreateInstance(qrModalEl);
    if (modalInstance) {
      modalInstance.show();
    }
  }

  const idleView = document.getElementById('snapshot-idle-view');
  const previewView = document.getElementById('snapshot-preview-view');
  const previewImg = document.getElementById('snapshot-preview-img');
  const resultsDiv = document.getElementById('qr-reader-results');
  const retakeWrapper = document.getElementById('snapshot-retake-wrapper');
  const laserBeam = document.getElementById('snapshot-laser');

  // Render instantaneous preview
  if (idleView) idleView.classList.add('d-none');
  if (previewView) previewView.classList.remove('d-none');
  if (laserBeam) laserBeam.style.display = 'block';
  if (retakeWrapper) retakeWrapper.classList.add('d-none');
  if (previewImg) previewImg.classList.remove('qr-focused-zoom');

  try {
    const objectUrl = URL.createObjectURL(file);
    if (previewImg) {
      previewImg.src = objectUrl;
    }
  } catch (urlErr) {
    console.warn("ObjectURL creation failed:", urlErr);
  }

  if (resultsDiv) {
    resultsDiv.innerHTML = '<span class="text-info"><i class="fa-solid fa-spinner fa-spin me-1"></i> Focusing on QR code & analyzing...</span>';
  }

  isSnapshotProcessing = true;

  try {
    const imageBitmap = await createImageBitmap(file);
    const canvas = document.createElement('canvas');
    const maxDimension = 1200;
    let width = imageBitmap.width;
    let height = imageBitmap.height;

    if (width > maxDimension || height > maxDimension) {
      if (width > height) {
        height = Math.round((height * maxDimension) / width);
        width = maxDimension;
      } else {
        width = Math.round((width * maxDimension) / height);
        height = maxDimension;
      }
    }

    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(imageBitmap, 0, 0, width, height);

    // Pass 1: jsQR full pixel scan (strict ISO/IEC 18004 2D QR code engine)
    if (typeof jsQR !== 'undefined') {
      try {
        const imgData = ctx.getImageData(0, 0, width, height);
        const code = jsQR(imgData.data, imgData.width, imgData.height, {
          inversionAttempts: 'attemptBoth'
        });
        if (code && code.data && code.data.trim().length > 0) {
          console.log('⚡ jsQR Pass 1 detected QR code:', code.data);
          const loc = code.location;
          let croppedUrl = null;
          if (loc) {
            const minX = Math.min(loc.topLeftCorner.x, loc.bottomLeftCorner.x);
            const maxX = Math.max(loc.topRightCorner.x, loc.bottomRightCorner.x);
            const minY = Math.min(loc.topLeftCorner.y, loc.topRightCorner.y);
            const maxY = Math.max(loc.bottomLeftCorner.y, loc.bottomRightCorner.y);
            croppedUrl = cropAndFocusQRCode(canvas, { x: minX, y: minY, width: maxX - minX, height: maxY - minY });
          }
          handleSuccessfulScan(code.data, croppedUrl);
          return;
        }
      } catch (jsqrErr) {
        console.warn('jsQR scan pass warning:', jsqrErr);
      }
    }

    // Pass 2: Native Android/Chromium BarcodeDetector API (Strictly QR Code format)
    if ('BarcodeDetector' in window) {
      try {
        const barcodeDetector = new BarcodeDetector({ formats: ['qr_code'] });
        const barcodes = await barcodeDetector.detect(canvas);
        const qrOnlyMatches = (barcodes || []).filter(b => b.format === 'qr_code' || !b.format);
        if (qrOnlyMatches.length > 0 && qrOnlyMatches[0].rawValue) {
          console.log('⚡ BarcodeDetector Pass 2 detected QR code:', qrOnlyMatches[0].rawValue);
          const box = qrOnlyMatches[0].boundingBox;
          const croppedUrl = box ? cropAndFocusQRCode(canvas, box) : null;
          handleSuccessfulScan(qrOnlyMatches[0].rawValue, croppedUrl);
          return;
        }
      } catch (nativeErr) {
        console.warn('Native BarcodeDetector pass warning:', nativeErr);
      }
    }

    // Pass 3: Center Zoom 60% Crop Scan (Focuses in on center if QR code is framed in the center)
    if (typeof jsQR !== 'undefined') {
      try {
        const centerW = Math.round(width * 0.65);
        const centerH = Math.round(height * 0.65);
        const startX = Math.round((width - centerW) / 2);
        const startY = Math.round((height - centerH) / 2);
        const centerCanvas = document.createElement('canvas');
        centerCanvas.width = centerW;
        centerCanvas.height = centerH;
        const centerCtx = centerCanvas.getContext('2d');
        centerCtx.drawImage(canvas, startX, startY, centerW, centerH, 0, 0, centerW, centerH);
        const centerData = centerCtx.getImageData(0, 0, centerW, centerH);
        const centerCode = jsQR(centerData.data, centerW, centerH, { inversionAttempts: 'attemptBoth' });
        if (centerCode && centerCode.data && centerCode.data.trim().length > 0) {
          console.log('⚡ jsQR Pass 3 (Center Zoom) detected QR code:', centerCode.data);
          const loc = centerCode.location;
          let croppedUrl = null;
          if (loc) {
            const minX = Math.min(loc.topLeftCorner.x, loc.bottomLeftCorner.x);
            const maxX = Math.max(loc.topRightCorner.x, loc.bottomRightCorner.x);
            const minY = Math.min(loc.topLeftCorner.y, loc.topRightCorner.y);
            const maxY = Math.max(loc.bottomLeftCorner.y, loc.bottomRightCorner.y);
            croppedUrl = cropAndFocusQRCode(centerCanvas, { x: minX, y: minY, width: maxX - minX, height: maxY - minY });
          }
          handleSuccessfulScan(centerCode.data, croppedUrl);
          return;
        }
      } catch (zoomErr) {
        console.warn('Center zoom scan warning:', zoomErr);
      }
    }

    // Pass 4: Html5Qrcode ZXing file scanner (Strictly QR_CODE format)
    if (typeof Html5Qrcode !== 'undefined') {
      try {
        let tempScannerId = 'snapshot-temp-zxing';
        let tempDiv = document.getElementById(tempScannerId);
        if (!tempDiv) {
          tempDiv = document.createElement('div');
          tempDiv.id = tempScannerId;
          tempDiv.style.display = 'none';
          document.body.appendChild(tempDiv);
        }
        const formats = (typeof Html5QrcodeSupportedFormats !== 'undefined' && Html5QrcodeSupportedFormats.QR_CODE !== undefined)
          ? [ Html5QrcodeSupportedFormats.QR_CODE ]
          : undefined;
        const fileScanner = new Html5Qrcode(tempScannerId, formats ? { formatsToSupport: formats } : undefined);
        const decodedText = await fileScanner.scanFile(file, false);
        if (decodedText && decodedText.trim().length > 0) {
          console.log('⚡ Html5Qrcode ZXing Pass 4 detected QR code:', decodedText);
          handleSuccessfulScan(decodedText);
          return;
        }
      } catch (zxingErr) {
        console.warn('Html5Qrcode scan pass warning:', zxingErr);
      }
    }

    // Pass 5: Grayscale + High-Contrast Binarization Filter for jsQR
    if (typeof jsQR !== 'undefined') {
      try {
        const imgData = ctx.getImageData(0, 0, width, height);
        const d = imgData.data;
        for (let i = 0; i < d.length; i += 4) {
          const gray = (d[i] * 0.299 + d[i + 1] * 0.587 + d[i + 2] * 0.114);
          const binarized = gray > 128 ? 255 : 0;
          d[i] = binarized;
          d[i + 1] = binarized;
          d[i + 2] = binarized;
        }
        ctx.putImageData(imgData, 0, 0);
        const code = jsQR(d, width, height, { inversionAttempts: 'attemptBoth' });
        if (code && code.data && code.data.trim().length > 0) {
          console.log('⚡ jsQR Pass 5 Contrast Filter detected QR code:', code.data);
          const loc = code.location;
          let croppedUrl = null;
          if (loc) {
            const minX = Math.min(loc.topLeftCorner.x, loc.bottomLeftCorner.x);
            const maxX = Math.max(loc.topRightCorner.x, loc.bottomRightCorner.x);
            const minY = Math.min(loc.topLeftCorner.y, loc.topRightCorner.y);
            const maxY = Math.max(loc.bottomLeftCorner.y, loc.bottomRightCorner.y);
            croppedUrl = cropAndFocusQRCode(canvas, { x: minX, y: minY, width: maxX - minX, height: maxY - minY });
          }
          handleSuccessfulScan(code.data, croppedUrl);
          return;
        }
      } catch (filterErr) {
        console.warn('Contrast filter pass warning:', filterErr);
      }
    }

  } catch (err) {
    console.error('Snapshot photo processing error:', err);
  }

  // If all passes failed to detect
  if (laserBeam) laserBeam.style.display = 'none';
  if (resultsDiv) {
    resultsDiv.innerHTML = '<span class="text-danger"><i class="fa-solid fa-triangle-exclamation me-1"></i> No QR code detected in this photo. Please retake closer to the driver\'s QR badge.</span>';
  }
  if (retakeWrapper) {
    retakeWrapper.classList.remove('d-none');
  }
}

/**
 * Handle successful QR scan decoding with auto-cropped focus preview and redirection.
 */
function handleSuccessfulScan(decodedText, croppedImageUrl) {
  const resultsDiv = document.getElementById('qr-reader-results');
  const previewImg = document.getElementById('snapshot-preview-img');
  const laserBeam = document.getElementById('snapshot-laser');
  
  if (laserBeam) laserBeam.style.display = 'none';

  // Apply auto-cropped focused image preview with zoom animation
  if (croppedImageUrl && previewImg) {
    previewImg.src = croppedImageUrl;
    previewImg.classList.add('qr-focused-zoom');
  }

  if (resultsDiv) {
    resultsDiv.innerHTML = '<span class="text-success fw-bold fs-6"><i class="fa-solid fa-circle-check fa-bounce me-1"></i> QR Code Focused & Verified! Redirecting...</span>';
  }

  // Play subtle haptic feedback on mobile if supported
  if (navigator.vibrate) {
    try { navigator.vibrate([80, 40, 80]); } catch (e) {}
  }

  // Close modal and navigate after brief visual focus confirmation
  const qrModalEl = document.getElementById('qrScannerModal');
  const trimmed = (decodedText || '').trim();

  setTimeout(() => {
    if (qrModalEl && typeof bootstrap !== 'undefined') {
      const modalInstance = bootstrap.Modal.getInstance(qrModalEl);
      if (modalInstance) {
        modalInstance.hide();
      }
    }

    // 1. If scanned text is a URL containing /verify/
    if (trimmed.startsWith('http://') || trimmed.startsWith('https://')) {
      try {
        const urlObj = new URL(trimmed);
        if (urlObj.pathname.includes('/verify/')) {
          window.location.href = window.location.origin + urlObj.pathname + urlObj.search;
          return;
        }
      } catch (e) {
        console.warn("URL parse error:", e);
      }
      window.location.href = trimmed;
      return;
    }

    // 2. Relative URL
    if (trimmed.startsWith('/')) {
      window.location.href = trimmed;
      return;
    }

    // 3. UUID token pattern (e.g. 48b111a2-3c22-4d89-9189-e58f2780e0c0 or 32 hex chars)
    if (/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(trimmed) || /^[0-9a-f]{32}$/i.test(trimmed)) {
      window.location.href = '/verify/' + encodeURIComponent(trimmed) + '/';
      return;
    }

    // 4. Vehicle Registration Number / License / Name query
    window.location.href = '/verify/?query=' + encodeURIComponent(trimmed);
  }, 600);
}

// Backward compatibility aliases
function startSafeRideScanner() {
  resetSnapshotScanner();
}
function stopSafeRideScanner() {
  resetSnapshotScanner();
}
function initializeQRScanner(onScanSuccessCallback) {
  resetSnapshotScanner();
}

// Interactive Live Trip Google Maps Initializer
function initializeLiveTripMap(mapElementId, lat, lng, driverName, vehicleNo) {
  const mapElement = document.getElementById(mapElementId);
  if (!mapElement) return null;

  if (typeof google === 'undefined' || !google.maps) {
    console.warn("Google Maps JavaScript API not loaded or pending API key.");
    return null;
  }

  const pos = { lat: parseFloat(lat), lng: parseFloat(lng) };
  const map = new google.maps.Map(mapElement, {
    zoom: 15,
    center: pos,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: false,
    zoomControl: true,
    styles: [
      { elementType: "geometry", stylers: [{ color: "#1e293b" }] },
      { elementType: "labels.text.stroke", stylers: [{ color: "#0f172a" }] },
      { elementType: "labels.text.fill", stylers: [{ color: "#94a3b8" }] },
      { featureType: "road", elementType: "geometry", stylers: [{ color: "#334155" }] },
      { featureType: "road", elementType: "labels.text.fill", stylers: [{ color: "#f8fafc" }] },
      { featureType: "water", elementType: "geometry", stylers: [{ color: "#0f172a" }] }
    ]
  });

  const marker = new google.maps.Marker({
    position: pos,
    map: map,
    title: `${vehicleNo} - ${driverName}`,
    icon: {
      path: google.maps.SymbolPath.CIRCLE,
      scale: 10,
      fillColor: "#2563EB",
      fillOpacity: 1,
      strokeColor: "#FFFFFF",
      strokeWeight: 2
    }
  });

  const infoWindow = new google.maps.InfoWindow({
    content: `
      <div style="color: #0F172A; font-family: Inter, sans-serif; padding: 4px;">
        <h6 style="margin: 0; font-weight: bold; color: #1E3A8A;">${vehicleNo}</h6>
        <p style="margin: 4px 0 0 0; font-size: 13px;">Driver: ${driverName}</p>
        <span style="display:inline-block; background: #065F46; color: white; padding: 2px 6px; border-radius: 4px; font-size: 11px; font-weight: bold; margin-top: 4px;">SafeRide Monitored</span>
      </div>
    `
  });

  infoWindow.open(map, marker);
  marker.addListener("click", () => {
    infoWindow.open(map, marker);
  });

  return { map, marker, infoWindow };
}

// Toggle Password Visibility (Show/Hide with Eye Icon)
function togglePasswordVisibility(inputId = 'id_password', iconId = 'togglePasswordIcon') {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);
  if (input && icon) {
    if (input.type === 'password') {
      input.type = 'text';
      icon.classList.remove('fa-eye');
      icon.classList.add('fa-eye-slash');
    } else {
      input.type = 'password';
      icon.classList.remove('fa-eye-slash');
      icon.classList.add('fa-eye');
    }
  }
}

// ==========================================
// SCREEN WAKE LOCK API & PWA SERVICE WORKER
// ==========================================

let globalScreenWakeLock = null;

/**
 * Request Screen Wake Lock during active trips to prevent screen auto-lock/sleep
 * and avoid browser background JavaScript throttling.
 */
async function requestScreenWakeLock() {
  if ('wakeLock' in navigator) {
    try {
      globalScreenWakeLock = await navigator.wakeLock.request('screen');
      console.log('📱 Screen Wake Lock active: screen will remain on for continuous GPS & SOS monitoring.');
      globalScreenWakeLock.addEventListener('release', () => {
        console.log('📱 Screen Wake Lock released.');
      });
    } catch (err) {
      console.warn('Screen Wake Lock request failed:', err.message);
    }
  }
}

/**
 * Re-acquire Screen Wake Lock when switching back to tab/browser from background.
 */
document.addEventListener('visibilitychange', async () => {
  if (globalScreenWakeLock !== null && document.visibilityState === 'visible') {
    await requestScreenWakeLock();
  }
});

/**
 * Release the Screen Wake Lock when trip ends or user leaves active trip.
 */
function releaseScreenWakeLock() {
  if (globalScreenWakeLock !== null) {
    globalScreenWakeLock.release().then(() => {
      globalScreenWakeLock = null;
    }).catch(e => console.warn(e));
  }
}

/**
 * SafeRide PWA Service Worker Registration
 */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => console.log('🛡️ SafeRide PWA Service Worker Registered. Scope:', reg.scope))
      .catch((err) => console.warn('PWA Service Worker registration warning:', err));
  });
}

