# HumanFlow Tracker - AI-Powered People Counting System

A real-time computer vision system that automatically counts people entering and exiting retail stores using YOLO object detection and custom tracking algorithms. Features WhatsApp notifications for shop owners and managers.

<img width="1017" height="522" alt="image" src="https://github.com/user-attachments/assets/7e68affd-5124-4404-b06b-e9b8005e47f1" />

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-green.svg)
![YOLO](https://img.shields.io/badge/YOLO-11-orange.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🎯 Features

- **Real-time People Detection**: Uses YOLO11 for accurate person detection
- **Entry/Exit Tracking**: Custom tracking algorithm with polygon-based zones
- **WhatsApp Notifications**: Instant alerts via Twilio integration
- **Video Processing**: Supports live camera feeds and video files
- **Analytics Display**: Real-time counters and visual feedback
- **Easy Configuration**: Simple setup with configurable detection zones

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam or video file
- (Optional) Twilio account for WhatsApp notifications

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/smartshop-counter.git
cd smartshop-counter
```

2. **Create virtual environment**
```bash
python -m venv yolovenv
# On Windows:
yolovenv\Scripts\activate
# On macOS/Linux:
source yolovenv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download YOLO model** (automatically downloaded on first run)
```bash
# The YOLO11n.pt model will be downloaded automatically
```

### Usage

#### Basic People Counting
```bash
python object_count.py
```

#### With WhatsApp Notifications
```bash
python object_count_with_notifications.py
```

## 📋 Requirements

- opencv-python
- numpy
- ultralytics
- twilio (for notifications)

## ⚙️ Configuration

### Detection Zones

The system uses two polygon zones for entry/exit detection:

```python
# Zone 1: Entry detection area
area1 = [(312, 388), (289, 390), (474, 469), (497, 462)]

# Zone 2: Exit detection area  
area2 = [(279, 392), (250, 397), (423, 477), (454, 469)]
```

### WhatsApp Notifications Setup

1. Create a Twilio account at [twilio.com](https://www.twilio.com)
2. Get your Account SID and Auth Token
3. Set up environment variables:

```bash
# Create .env file
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone
TARGET_PHONE_NUMBER=recipient_phone_number
```

## 🎮 Controls

- **ESC**: Exit the application
- **R**: Reset notification tracking (notifications version only)
- **Mouse**: Click to get coordinates for zone configuration

## 📊 How It Works

1. **Person Detection**: YOLO11 model detects people in the video frame
2. **Object Tracking**: Custom algorithm tracks individuals across frames
3. **Zone Analysis**: Checks if tracked persons cross defined entry/exit zones
4. **Counting Logic**: 
   - Person enters Zone 2 → marked as "entering"
   - Person from Zone 2 enters Zone 1 → counted as "entered"
   - Person enters Zone 1 → marked as "exiting" 
   - Person from Zone 1 enters Zone 2 → counted as "exited"
5. **Notifications**: Sends WhatsApp alerts for new entries (if enabled)

## 🎥 Video Input

The system works with:
- Live camera feeds (webcam)
- Video files (MP4, AVI, etc.)
- RTSP streams

To use a different video source, modify the `VideoCapture` line:

```python
# For webcam
cap = cv2.VideoCapture(0)

# For video file
cap = cv2.VideoCapture("your_video.mp4")

# For RTSP stream
cap = cv2.VideoCapture("rtsp://your-stream-url")
```

## 📈 Output

The system displays:
- Real-time video feed with bounding boxes
- Entry/exit counters
- Zone visualization
- Person IDs and tracking
- Notification status

## 🔧 Customization

### Adjusting Detection Sensitivity

```python
# In tracker.py
tracker = Tracker(distance_threshold=25)  # Lower = more sensitive
```

### Changing Model

```python
# Use different YOLO model
model = YOLO("yolo11s.pt")  # or yolo11m.pt, yolo11l.pt, yolo11x.pt
```

### Modifying Zones

Use the mouse callback to get coordinates:
1. Run the application
2. Move mouse over desired zone corners
3. Note the coordinates printed in console
4. Update the area1 and area2 arrays

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'ultralytics'"**
```bash
pip install ultralytics
```

**"Camera not found"**
- Check camera permissions
- Try different camera index (0, 1, 2...)
- Verify camera is not used by other applications

**"WhatsApp notifications not working"**
- Verify Twilio credentials
- Check phone number format (+1234567890)
- Ensure Twilio account has sufficient balance

**"Poor detection accuracy"**
- Ensure good lighting conditions
- Adjust detection zones
- Try different YOLO model size

## 📁 Project Structure

```
humanflow-tracker/
├── object_count.py                    # Basic counting system
├── object_count_with_notifications.py # With WhatsApp alerts
├── tracker.py                        # Custom tracking algorithm
├── requirements.txt                  # Python dependencies
├── env_example.txt                   # Environment variables template
├── outside_shop.mp4                  # Sample video
├── yolovenv/                         # Virtual environment
└── README.md                         # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ultralytics](https://github.com/ultralytics/ultralytics) for YOLO implementation
- [OpenCV](https://opencv.org/) for computer vision capabilities
- [Twilio](https://www.twilio.com/) for WhatsApp integration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/smartshop-counter/issues) page
2. Create a new issue with detailed description
3. Include system information and error logs

---

**Made with ❤️ for retail businesses**
