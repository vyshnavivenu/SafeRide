# SAFERIDE: Driver Verification & Passenger Safety System

---

## 📌 1. Project Overview & Abstract

**SafeRide** is a centralized, web-based platform engineered to establish passenger safety and accountability in informal transit services (auto-rickshaws, local taxis, and shared cabs). The system connects **Passengers**, **Drivers**, and **Administrators** to eliminate travel uncertainty via:
1. **On-the-spot Driver & Vehicle Verification**: Scan QR codes or enter vehicle registration plates to instantly view verified driver credentials.
2. **Dynamic Reputation Score Algorithm**: Multi-criteria scoring computed from passenger ratings, trip volume, document verification, and complaint infractions.
3. **1-Touch SOS Emergency Alert Broadcast**: Immediate GPS telemetry transmission to the Central Admin Command Center and automated dispatch links for emergency contacts.
4. **Administrative KYC & Redressal**: Rigorous document validation before issuing QR codes and structured grievance handling with reputation penalties.

---

## 🚀 2. Instant Zero-Hassle Quickstart

To run the platform locally with all pre-seeded demo drivers, QR codes, and test accounts:

### Method A: Single-Click Launch (Windows)
Double-click **`run_server.bat`** in the project folder.

### Method B: Command Line Launch
```bash
# 1. Run migrations
python manage.py makemigrations core
python manage.py migrate

# 2. Seed demo drivers, vehicles, QR codes, and test accounts
python core/seed_data.py

# 3. Start development server
python manage.py runserver
```
Open **`http://127.0.0.1:8000`** in Google Chrome or Mozilla Firefox.

---

## 🔑 3. Pre-Configured Test Credentials

| Role | Username | Password | Notes & Features |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Access to Central Command Center, Driver KYC approvals, Real-time SOS dispatch, and Grievance management. |
| **Passenger** | `vyshnavi` | `passenger123` | Configured with emergency contacts, journey history, 1-touch SOS, and rating submission. |
| **Passenger (Alternative)** | `rahul` | `passenger123` | Secondary test passenger account. |
| **Verified Auto Driver** | `driver_rajesh` | `driver123` | Vehicle: `KL-05-AT-4455` (Bajaj RE, 96.5 Score, Active QR code). |
| **Verified Taxi Driver** | `driver_anand` | `driver123` | Vehicle: `KL-05-TX-1024` (Dzire, 94.0 Score, Active QR code). |
| **Pending KYC Driver** | `driver_vinod` | `driver123` | Vehicle: `KL-05-AT-9911` (Awaiting Admin document review). |

---

## 🛠️ 4. Technology Stack

- **Frontend & Mapping**: HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6+), Google Maps JavaScript API (Places, Geocoding & Geometry) + Leaflet.js (OpenStreetMap Hybrid Fallback), html5-qrcode
- **Backend**: Python 3.12, Django 5.x (MVC Architecture, ORM, Session Security)
- **REST APIs**: Django REST Framework (DRF)
- **Database**: MySQL 8.x / MariaDB (managed via XAMPP & phpMyAdmin)
- **QR Code Engine**: Python `qrcode` + Pillow

---

## 📂 5. Project Module Breakdown

- **Module 1**: Authentication & Role-Based Access Control (`PASSENGER`, `DRIVER`, `ADMIN`)
- **Module 2**: Driver Registration, Document KYC & Administrative Verification
- **Module 3**: In-Browser QR Code Camera Scanner & Driver Safety Card Display
- **Module 4**: Intelligent Multi-Factor Reputation Engine & Safety Reviews
- **Module 5**: 1-Touch SOS Emergency Alert, GPS Telemetry & Live Map Share Link
- **Module 6**: Incident Reporting & Complaint Resolution Workflow
- **Module 7**: Central Administrator Command & Live Emergency Monitoring Dashboard
- **Module 8**: Django REST Framework API Endpoints (`/api/v1/...`)
