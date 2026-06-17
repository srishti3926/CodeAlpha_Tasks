# 🚀 Real-Time Object Detection & Tracking with YOLOv8

A real-time computer vision project that performs **object detection and multi-object tracking** using **YOLOv8**, **ByteTrack**, and **OpenCV**. The system supports both webcam and video inputs and displays object labels, tracking IDs, FPS, and class-wise statistics in real time.

## ✨ Features

- 🎯 Real-time object detection with YOLOv8
- 🔄 Multi-object tracking using ByteTrack
- 📹 Supports webcam and video files
- 🆔 Persistent tracking IDs
- 📊 Live FPS monitoring and object count
- 🏷️ Optional confidence score display
- 🎨 Color-coded bounding boxes and labels
- ⚡ Fast and lightweight implementation

## 🛠️ Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- ByteTrack

## 📂 Project Structure

```
├── detect.py
├── requirements.txt
├── yolov8s.pt
└── slideshow.gif
```

## 📦 Installation

### 1️⃣ Create a Virtual Environment

```bash
python -m venv yolo_env
```

### 2️⃣ Activate the Environment

**Windows**

```bash
yolo_env\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Install Required Packages

```bash
pip install ultralytics opencv-python
