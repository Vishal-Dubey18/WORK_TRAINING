# 🌟 Smart Tracking System

## 📋 Overview

The **Smart Tracking System** is a cutting-edge facial recognition application designed to:
- Identify known individuals with precision.
- Alert users when an unknown face is detected.
- Mark attendance with timestamps for known individuals.

This project leverages:
- `face_recognition` for robust facial recognition.
- OpenCV for real-time image processing.
- Gmail for seamless email notifications.

---

## 👥 Authors

- **HackBeyond** ([vdubey8511@gmail.com](mailto:vdubey8511@gmail.com))
- **Vishal**

---

## 🚀 Features

- 🎯 **Facial Recognition**: Accurate identification of known faces.
- 🛡️ **Unknown Face Detection**: Captures and stores images of unrecognized faces.
- 📧 **Email Alerts**: Instantly notifies via email when an unknown face is detected.
- 🕒 **Attendance Tracking**: Maintains a detailed log of recognized individuals.

---

## 🛠️ Requirements

Ensure you have the following installed:

- Python 3.x
- OpenCV
- NumPy
- face_recognition
- smtplib (for email notifications)

Install dependencies:

```bash
pip install opencv-python numpy face_recognition
```

---

## ⚙️ Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Vishal-Dubey18/file.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd PROJECT/SMART_TRACKING_SYSTEM
   ```

3. **Prepare Known Images**:
   - Place JPEG images of known individuals in the `IMAGES_KNOWN` directory.

4. **Prepare Unknown Images Directory**:
   - Ensure the `IMAGES_UNKNOWN` directory exists for saving images of unrecognized faces.

5. **Configure Email Alerts**:
   - Update the `EMAIL_CONFIG` in the `Tracking.py` file with your Gmail credentials and app password.

6. **Run the Application**:

   ```bash
   python Tracking.py
   ```

---

## 🎮 Usage

- The application opens your webcam and begins face detection.
- **Green Rectangle**: Marks recognized faces with their names.
- **Red Rectangle**: Flags unknown faces and sends an email alert.
- Press `q` to exit the application.

---

## 📁 File Structure

```
SMART_TRACKING_SYSTEM/
│
├── IMAGES_KNOWN/          # Directory for known faces
│   ├── abhi.jpeg
│   ├── anish.jpeg
│   ├── harsh.jpeg
│   ├── priyanshu.jpeg
│   └── shivam.jpeg
│
├── IMAGES_UNKNOWN/        # Directory for unknown faces
│
├── att.csv                # Attendance log
│
└── Tracking.py            # Main application script
```

---

## ❓ Troubleshooting

- ✅ Ensure your webcam is functioning correctly.
- ✅ Verify image directory paths.
- ✅ For email issues, double-check your Gmail app password and email settings.
- ✅ Make sure you have created an app password for your Gmail account if 2FA is enabled.

---

## 📜 License

This project is licensed under the **MIT License**. See the `LICENSE` file for more details.

---

## 🙌 Acknowledgments

- **face_recognition**: Powering facial recognition.
- **OpenCV**: Enabling real-time computer vision.
- **Gmail**: Handling email notifications effortlessly.

---

## 📬 Contact

For inquiries or feedback:
- **HackBeyond**: [vdubey8511@gmail.com](mailto:vdubey8511@gmail.com)
- **Vishal**

---

## 🔗 GitHub Repository

Find the project repository here: [Smart Tracking System GitHub](https://github.com/Vishal-Dubey18/file.git)
```

This README file provides comprehensive information about your project, including setup instructions, features, and troubleshooting tips. It should help users understand and run the Smart Tracking System application successfully.