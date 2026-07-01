# 🐘 SEDS v2

## Smart Elephant Intrusion Detection System

### Edge AI Wildlife Monitoring Platform
Project Description
SEDS v2 is an Edge AI wildlife monitoring platform designed for deployment on Raspberry Pi devices. The system performs real-time object detection using YOLOv8, applies configurable decision rules, aggregates intrusion events, stores evidence locally, and provides analytics through an interactive Streamlit dashboard.
## Features

- Real-time wildlife detection using YOLOv8
- Modular software architecture
- Event-based intrusion aggregation
- SQLite detection database
- Automatic evidence storage
- Confidence threshold filtering
- Interactive Streamlit dashboard
- Detection analytics
- Raspberry Pi ready
- Extensible IoT architecture
  
# Technology Features
| Layer                | Technology   |
| -------------------- | ------------ |
| Programming Language | Python 3.11  |
| Computer Vision      | OpenCV       |
| Object Detection     | YOLOv8       |
| Machine Learning     | Ultralytics  |
| Database             | SQLite       |
| Dashboard            | Streamlit    |
| Data Analysis        | Pandas       |
| Visualization        | Plotly       |
| Version Control      | Git + GitHub |

System Architecture
                Camera / Image
                       │
                       ▼
                OpenCV Processing
                       │
                       ▼
                  YOLOv8 Detector
                       │
                       ▼
               DetectionEvent Model
                       │
                       ▼
                 Rules Engine
                       │
                       ▼
                 Event Manager
                       │
                       ▼
              Detection Service
                │            │
                ▼            ▼
          SQLite Database   Logger
                │
                ▼
          Analytics Manager
                │
                ▼
         Streamlit Dashboard


#Folder Structure
SEDS_V2/
│
├── app/
├── config/
├── dashboard/
├── database/
├── detection/
├── decision/
├── storage/
├── tests/
├── docs/
├── captures/
└── test_images/

## Dashboard

Current pages:

- Home
- Detection History
- Analytics

Future pages:

- Evidence Viewer
- Settings
- Live Camera
  
## Development Status

- [x] Configuration Management
- [x] Logging Framework
- [x] SQLite Database
- [x] Detection Event Model
- [x] Detection Service
- [x] Mock Pipeline
- [x] OpenCV Integration
- [x] Visualization
- [x] Rules Engine
- [x] YOLOv8 Integration
- [x] Event Aggregation
- [x] Evidence Storage
- [x] Analytics
- [x] Dashboard
- [ ] Video Processing
- [ ] Telegram Alerts
- [ ] Cloud Logging
- [ ] Raspberry Pi Deployment
- [ ] Active Learning

#Future Roadmap
v2.0.0-alpha
Core Platform

↓

v2.1
Dashboard Complete

↓

v2.2
Video Processing

↓

v2.3
Cloud Sync

↓

v2.4
Telegram Alerts

↓

v2.5
Raspberry Pi Deployment

↓

v3.0
Active Learning

#Author
## Author

**Sadique Ul Hussain**

M.Tech (Computer Engineering)

National Institute of Technology Kurukshetra

GitHub: github.com/sadique786
