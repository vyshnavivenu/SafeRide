# SAFERIDE: Driver Verification & Passenger Safety System

---

## 📌 1. Project Overview & Abstract

**SafeRide** is a centralized, web-based platform engineered to establish passenger safety and accountability in informal transit services (auto-rickshaws, local taxis, and shared cabs). The system connects **Passengers**, **Drivers**, and **Administrators** to eliminate travel uncertainty through instant QR code driver verification, continuous journey telemetry, 1-touch emergency SOS broadcasting, and administrative KYC enforcement.

---

## 📂 2. Official System Modules

### 👤 1. PASSENGER MODULE
- **Register and Login**: Passengers create an account and securely log in to access the system.
- **Verify Driver**: Passengers scan the driver's QR code or enter the vehicle number to verify the driver's identity, vehicle details, verification status, and reputation before starting the trip.
- **View Driver Reputation**: Passengers can view ratings and reviews submitted by previous passengers.
- **Share Live Location**: Passengers can share their current GPS location during the trip for improved safety.
- **SOS Alert**: When the SOS button is pressed, the system immediately sends an emergency alert containing the passenger's live location, driver details, and trip information to the Administrator Dashboard for immediate action.
- **Submit Ratings & Complaints**: Passengers can rate drivers and submit complaints after completing the trip.

### 🚖 2. DRIVER MODULE
- **Login**: Registered drivers securely log in to access their account and available system services.
- **Verification Status**: The administrator reviews the submitted documents and updates the verification status as Pending, Verified, or Rejected. Only verified drivers can access all system services.
- **Generate QR Code**: After successful verification, the system automatically generates a unique QR code linked to the verified driver profile.
- **Manage Profile**: Drivers can update their personal and vehicle information.
- **View Ratings**: Drivers can monitor passenger ratings and feedback to improve service quality.

### 🛡️ 3. ADMINISTRATOR MODULE
- **Admin Login**: The administrator securely logs in to access system management features.
- **Centralized Dashboard**: Manage passengers, drivers, complaints, ratings, driver verification requests, and emergency alerts from a single dashboard.
- **Register & Manage Drivers**: The administrator directly registers new drivers by inputting their personal information, driving license details, vehicle information, and supporting documents into the system.
- **Manage Passengers**: View, edit, suspend, or remove passenger accounts when necessary.
- **Verify Drivers & Vehicles**: Validate driver identity, driving licence, and vehicle documents before approving or rejecting registration requests.
- **View Ratings & Feedback**: View passenger ratings and feedback submitted for drivers to monitor service quality and identify recurring issues.
- **Monitor Complaints**: Review complaints, investigate reported issues, and update their status.
- **Handle SOS Alerts**: Receive emergency alerts with passenger location, driver details, and trip information, coordinate assistance, and record the incident.

### 🔍 4. DRIVER VERIFICATION MODULE
- **Driver Verification**: The administrator verifies driver identity, driving licence, and vehicle documents. After successful approval, the system generates a unique QR code that passengers can scan to verify the driver's identity, vehicle details, verification status, and reputation before boarding.

### 🚨 5. EMERGENCY SAFETY MODULE
- **Live Location Tracking**: The system tracks the passenger's GPS location during the trip to support safety monitoring.
- **SOS Alerts**: When activated, the system creates an emergency alert containing the passenger's live location, driver details, and trip information and immediately sends it to the Administrator Dashboard.
- **Incident Reporting**: Passengers can report accidents, harassment, unsafe driving, or misconduct. The report is stored in the database and forwarded to the administrator for investigation and resolution.

---

## 🗄️ 3. Database Table Structure (The 9 Core Tables)

1. **`tbl_passenger`**: Stores passenger accounts, contact numbers, credentials, and trusted emergency contact.
2. **`tbl_driver`**: Stores driver details, vehicle registration, license numbers, KYC verification status, and reputation scores.
3. **`tbl_admin`**: Stores system administrator credentials and access.
4. **`tbl_vehicle_documents`**: Stores uploaded KYC documents (Driving License and RC Book files).
5. **`tbl_trip`**: Stores active and completed journey sessions, boarding & destination telemetry, and live coordinates.
6. **`tbl_rating_review`**: Stores passenger star ratings (1–5) and written feedback for drivers.
7. **`tbl_complaint`**: Stores passenger grievances against drivers and disciplinary penalty tracking.
8. **`tbl_sos_alert`**: Stores real-time emergency distress events, live GPS coordinates, and administrative response logs.
9. **`tbl_incident_report`**: Stores formal accident and safety hazard reports.

---

## 🚀 4. Quickstart & Local Setup

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
Open **`http://127.0.0.1:8000`** in your browser.

---

## 🔑 5. Pre-Configured Test Credentials

| Role | Username | Password | Key Capability |
| :--- | :--- | :--- | :--- |
| **System Administrator** | `admin` | `admin123` | Central Command Center, Driver KYC approvals, Live SOS dispatch, Grievance management |
| **Passenger** | `vyshnavi` | `passenger123` | Driver QR verification, 1-touch SOS, Journey logging, Rating submission |
| **Passenger (Alt)** | `rahul` | `passenger123` | Secondary test passenger account |
| **Verified Auto Driver** | `driver_rajesh` | `driver123` | Vehicle: `KL-05-AT-4455` (Bajaj RE, 96.5 Reputation, Active QR code) |
| **Verified Taxi Driver** | `driver_anand` | `driver123` | Vehicle: `KL-05-TX-1024` (Dzire, 94.0 Reputation, Active QR code) |
| **Pending KYC Driver** | `driver_vinod` | `driver123` | Vehicle: `KL-05-AT-9911` (Awaiting Admin document review) |

---

## 🛠️ 6. Technology Stack

- **Frontend & Mapping**: HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6+), Leaflet.js / Google Maps API, `html5-qrcode`
- **Backend**: Python 3.12, Django 5.x (MVC Architecture, ORM, Session Security)
- **REST APIs**: Django REST Framework (DRF)
- **Database**: MySQL 8.x / MariaDB (managed via XAMPP & phpMyAdmin)
- **QR Code Engine**: Python `qrcode` + Pillow
