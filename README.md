# 🛰️ Sat Map - AI-Powered Environmental Monitoring Platform

<img width="1919" height="1093" alt="image" src="https://github.com/user-attachments/assets/c515211e-c571-4fd6-afce-4117fe7a4838" />

![Python](https://img.shields.io/badge/Python-62.4%25-blue)
![HTML](https://img.shields.io/badge/HTML-37.6%25-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌍 Overview

**Sat Map** is an innovative AI-powered environmental monitoring platform that leverages satellite imagery and machine learning to detect environmental hazards, assess water quality, and provide actionable insights for sustainable development. The platform directly supports **UN Sustainable Development Goals (SDGs) 3, 6, and 11** by providing real-time environmental monitoring and risk assessment capabilities.

## ✨ Key Features

- **🤖 AI Trash Detection**: Advanced YOLO-based computer vision for identifying and categorizing different types of waste in satellite/drone imagery
- **💧 Water Quality Analysis**: Automated assessment of water contamination and quality from aerial imagery
- **⚠️ Real-time Risk Assessment**: Environmental health risk modeling and prediction system
- **🗺️ Interactive Mapping**: Web-based dashboard with heatmaps, hotspot identification, and layer controls
- **🎮 Gamification System**: Reward-based community engagement for environmental monitoring
- **📊 Environmental Impact Analytics**: Comprehensive reporting on waste generation patterns and environmental costs
- **🔔 Smart Alerts**: Automated notification system for environmental hazards

## 🏗️ Architecture

### Backend (FastAPI)
```
backend/
├── main.py                    # FastAPI application entry point
├── requirements.txt           # Python dependencies
├── yolov8n.pt                # Pre-trained YOLO model
├── models/                   # AI/ML Models
│   ├── trash_detector.py     # YOLO-based trash detection
│   ├── water_quality.py      # Water quality analysis
│   └── risk_model.py         # Environmental risk assessment
├── routes/                   # API Endpoints
│   ├── upload.py             # Image upload and processing
│   ├── map_data.py           # Geospatial data management
│   ├── alerts.py             # Alert system
│   └── gamification.py       # User engagement features
└── utils/                    # Utilities and configuration
```

### Frontend (HTML/JavaScript)
```
frontend/
└── build/
    └── index.html            # Interactive dashboard
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- FastAPI
- PyTorch
- OpenCV
- PIL (Pillow)
- Other dependencies listed in `requirements.txt`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/seerprime/sat_map.git
   cd sat_map
   ```

2. **Set up the backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file with your configuration
   cp .env.example .env
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/api/docs`.

## 📋 API Endpoints

### Core Analysis Endpoints

- **POST** `/api/upload/detect-trash` - AI-powered trash detection in images
- **POST** `/api/upload/analyze-water` - Water quality analysis from imagery  
- **POST** `/api/upload/combined-analysis` - Comprehensive environmental assessment
- **GET** `/api/upload/supported-formats` - List of supported file formats

### Map Data & Visualization

- **GET** `/api/map/hotspots` - Environmental hotspot identification
- **GET** `/api/map/heatmap-data` - Data for heatmap visualization
- **POST** `/api/map/report-location` - Report environmental issues

### Alert System

- **GET** `/api/alerts/active` - Current environmental alerts
- **POST** `/api/alerts/subscribe` - Alert subscription management

### Gamification

- **POST** `/api/game/user-action` - Track user environmental actions
- **GET** `/api/game/leaderboard` - Community leaderboard
- **GET** `/api/game/achievements` - User achievements system

## 🔧 Configuration

Key configuration options in `utils/config.py`:

- **File Upload**: Maximum file size (10MB), supported formats (JPG, PNG, WebP)
- **AI Models**: YOLO model configuration, confidence thresholds
- **API Settings**: CORS configuration, rate limiting
- **Database**: Environmental data storage configuration

## 🎯 Supported Analysis Types

### Trash Detection
- **Detectable Items**: Plastic bottles, bags, food wrappers, cigarette butts, aluminum cans, glass bottles, paper cups, cardboard, organic waste, electronics
- **Output**: Item classification, confidence scores, bounding boxes, recycling recommendations
- **Features**: Weight estimation, environmental impact calculation

### Water Quality Analysis
- **Parameters**: Contamination detection, water quality indexing, health risk assessment
- **Input**: Satellite/drone imagery of water bodies
- **Output**: Quality scores, contamination types, health risk levels

### Risk Assessment
- **Capabilities**: Health risk modeling, environmental cost calculation, future trend prediction
- **Integration**: Combines trash detection and water quality data for comprehensive analysis

## 🌱 Environmental Impact

Sat Map contributes to environmental sustainability by:

- **SDG 3 (Good Health and Well-being)**: Early detection of environmental health hazards
- **SDG 6 (Clean Water and Sanitation)**: Water quality monitoring and contamination alerts
- **SDG 11 (Sustainable Cities and Communities)**: Urban waste management and environmental planning

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Roadmap

- [ ] **Mobile Application**: Native iOS/Android app for field data collection
- [ ] **Real-time Satellite Integration**: Live satellite feed processing
- [ ] **Advanced ML Models**: Custom-trained models for specific environmental hazards
- [ ] **Community Features**: Social sharing, collaborative monitoring
- [ ] **IoT Integration**: Integration with environmental sensors
- [ ] **Blockchain Verification**: Decentralized data verification system

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/seerprime/sat_map/issues)
- **Documentation**: [API Documentation](http://localhost:8000/api/docs) (when running locally)
- **Maintainer**: [@seerprime](https://github.com/seerprime)

## 🙏 Acknowledgments

- YOLO (You Only Look Once) for object detection framework
- FastAPI for the robust API framework
- OpenCV for computer vision capabilities
- The open-source community for various tools and libraries

---

**Built with ❤️ for a sustainable future** 🌍
