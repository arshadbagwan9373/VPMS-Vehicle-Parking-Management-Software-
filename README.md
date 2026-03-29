<div align="center">

<img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Tkinter-GUI-FF6B35?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white"/>
<img src="https://img.shields.io/badge/Twilio-SMS-F22F46?style=for-the-badge&logo=twilio&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

# 🅿️ Smart Parking Management System

### *Automate. Track. Notify. Simplify.*

> A Python-based desktop application that replaces manual parking registers with an intelligent, GUI-driven system — complete with real-time slot tracking, SMS notifications, and complete vehicle history.

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Screenshots](#-screenshots)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#-usage)
- [Database Schema](#-database-schema)
- [SMS Notifications](#-sms-notifications)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔍 Overview

The **Smart Parking Management System** is a fully-featured desktop application designed to digitize and streamline parking operations. It eliminates the need for manual registers by providing an intuitive GUI interface that handles vehicle entry/exit, real-time slot availability tracking across vehicle categories, automated SMS alerts to owners, and a complete historical log of all parking activity.

Whether you manage a small lot or a multi-category facility, this system gives you full control at a glance.

---

## ✨ Features

### 🔐 Secure Login
- Password-protected access to prevent unauthorized use
- Session management for operational security

### 🏠 Dashboard — Live Slot Overview
- Real-time display of **available vs. occupied** parking slots
- Categorized by vehicle type:
  - 🛵 **2-Wheeler** slots
  - 🚗 **4-Wheeler** slots
  - 🚛 **Heavy Vehicle** slots
- Instant visual feedback on parking capacity

### 🚘 Vehicle Entry
- Register incoming vehicles with:
  - Vehicle Number
  - Owner Name & Phone Number
  - Vehicle Type (2-Wheeler / 4-Wheeler / Heavy Vehicle)
  - Auto-assigned Slot Number
  - Entry Date & Time (auto-captured)
- Prevents double-entry and slot conflicts

### 🚪 Vehicle Exit
- Quick exit processing by vehicle number
- Automatic **parking fee calculation** based on duration
- Marks slot as available upon exit
- Triggers SMS notification to owner on exit

### 📊 Currently Parked Vehicles
- Live table view of all vehicles currently in the lot
- Displays: Vehicle No., Owner, Type, Slot, Entry Time
- Scrollable and easy-to-read interface

### 📜 Vehicle History
- Complete log of all past parking sessions
- Records include entry/exit times and fees paid
- Useful for audits and operational reporting

### 📱 SMS Notifications (Twilio Integration)
- Automated SMS sent to vehicle owner on:
  - **Entry** — slot number and entry time
  - **Exit** — duration parked and fee charged
- Improves transparency and customer trust

### 🗄️ Database Integration
- All data persisted in a relational database (MySQL)
- No data loss on application restart
- Reliable and consistent record keeping

---

## 📸 Screenshots

<table>
  <tr>
    <td align="center"><strong>🔐 Login Screen</strong></td>
    <td align="center"><strong>🏠 Dashboard</strong></td>
  </tr>
  <tr>
    <td><img src="screenshots/Screenshot 2024-03-12 184316.png" width="400"/></td>
    <td><img src="screenshots/Screenshot 2024-03-12 184421.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><strong>🚘 Vehicle Entry</strong></td>
    <td align="center"><strong>🚪 Vehicle Exit</strong></td>
  </tr>
  <tr>
    <td><img src="screenshots/Screenshot 2024-03-12 184503.png" width="400"/></td>
    <td><img src="screenshots/Screenshot 2024-03-12 184519.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><strong>📊 Currently Parked Vehicles</strong></td>
    <td align="center"><strong>📜 Vehicle History</strong></td>
  </tr>
  <tr>
    <td><img src="screenshots/Screenshot 2024-03-12 184753.png" width="400"/></td>
    <td><img src="screenshots/Screenshot 2024-03-12 184913.png" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><strong>📱 SMS Notification</strong></td>
    <td align="center"><strong>🅿️ Slot Availability</strong></td>
  </tr>
  <tr>
    <td><img src="screenshots/Screenshot 2024-03-12 185422.png" width="400"/></td>
    <td><img src="screenshots/Screenshot 2024-03-12 185232.png" width="400"/></td>
  </tr>
</table>

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| GUI Framework | Tkinter |
| Database | MySQL |
| SMS Service | Twilio API |
| DB Connector | `mysql-connector-python` |
| Date/Time | `datetime` module |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- MySQL Server
- A [Twilio account](https://www.twilio.com/) with an active phone number

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/smart-parking-management.git
cd smart-parking-management
```

**2. Install required dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up the database**
```bash
mysql -u root -p < database/parking_schema.sql
```

### Configuration

Edit `config.py` with your credentials:

```python
# Database Configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"
DB_NAME = "parking_db"

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = "your_account_sid"
TWILIO_AUTH_TOKEN = "your_auth_token"
TWILIO_PHONE_NUMBER = "+1XXXXXXXXXX"

# Parking Slot Capacity
SLOTS_TWO_WHEELER   = 20
SLOTS_FOUR_WHEELER  = 30
SLOTS_HEAVY_VEHICLE = 10

# Fee per hour (in ₹)
RATE_TWO_WHEELER    = 10
RATE_FOUR_WHEELER   = 20
RATE_HEAVY_VEHICLE  = 40
```

**4. Run the application**
```bash
python main.py
```

> **Default Login:** Username: `admin` | Password: `admin123`  
> *(Change these credentials after first login)*

---

## 💡 Usage

### Workflow

```
1. Launch app → Login with credentials
        ↓
2. Dashboard → View available slots by category
        ↓
3. Vehicle Entry → Fill in vehicle details → Submit
        ↓
   [SMS sent to owner: Entry confirmed + Slot number]
        ↓
4. Vehicle Exit → Enter vehicle number → Fee calculated → Confirm
        ↓
   [SMS sent to owner: Exit confirmed + Fee charged]
        ↓
5. View Reports → Currently Parked / Vehicle History tabs
```

---

## 🗄️ Database Schema

```sql
-- Vehicles Table
CREATE TABLE vehicles (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_no  VARCHAR(20) NOT NULL UNIQUE,
    owner_name  VARCHAR(100) NOT NULL,
    phone       VARCHAR(15) NOT NULL,
    type        ENUM('2-Wheeler', '4-Wheeler', 'Heavy') NOT NULL,
    slot_no     INT NOT NULL,
    entry_time  DATETIME DEFAULT CURRENT_TIMESTAMP,
    exit_time   DATETIME,
    fee         DECIMAL(10, 2),
    status      ENUM('Parked', 'Exited') DEFAULT 'Parked'
);

-- Slots Table
CREATE TABLE slots (
    slot_id     INT PRIMARY KEY,
    type        ENUM('2-Wheeler', '4-Wheeler', 'Heavy') NOT NULL,
    is_occupied BOOLEAN DEFAULT FALSE
);
```

---

## 📱 SMS Notifications

The system uses **Twilio** to send real-time SMS alerts. Notifications are automatically triggered on:

| Event | Message Content |
|---|---|
| Vehicle Entry | Slot number, entry time, vehicle number |
| Vehicle Exit | Duration parked, total fee, thank-you message |

**Twilio Setup:**
1. Sign up at [twilio.com](https://www.twilio.com)
2. Get your `Account SID` and `Auth Token` from the Console
3. Purchase or use a trial phone number
4. Add credentials to `config.py`

---

## 📁 Project Structure

```
smart-parking-management/
│
├── main.py                  # Application entry point
├── config.py                # Configuration (DB, Twilio, rates)
├── requirements.txt         # Python dependencies
│
├── gui/
│   ├── login.py             # Login screen
│   ├── dashboard.py         # Main dashboard with slot overview
│   ├── entry.py             # Vehicle entry form
│   ├── exit.py              # Vehicle exit & fee calculation
│   ├── parked.py            # Currently parked vehicles view
│   └── history.py           # Vehicle history view
│
├── database/
│   ├── db_connect.py        # Database connection handler
│   ├── operations.py        # CRUD operations
│   └── parking_schema.sql   # SQL schema
│
├── sms/
│   └── notify.py            # Twilio SMS integration
│
└── screenshots/             # Application screenshots
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

Please ensure your code follows [PEP 8](https://pep8.org/) style guidelines.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with ❤️ using Python & Tkinter

⭐ **If you found this useful, give it a star!** ⭐

</div>
