import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import smtplib
from email.message import EmailMessage
import time

path = r'F:\GIT_HUB\PROJECT\SMART_TRACKING_SYSTEM\IMAGES_KNOWN'
unknown_faces_path = r'F:\GIT_HUB\PROJECT\SMART_TRACKING_SYSTEM\IMAGES_UNKNOWN'
images = []
classNames = []
myList = os.listdir(path)
print(f"Images found: {myList}")

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(f"Class names: {classNames}")

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 465,
    'sender_email': 'vdubey8511@gmail.com',  # Replace with your email
    'sender_password': 'nogcmdrmgvgcrkik',  # Generated App Password
    'recipient_email': 'vdubey8511@gmail.com'  # Alert destination
}

# Performance optimizations
PROCESS_EVERY_N_FRAMES = 3  # Process every 3rd frame
DETECTION_THRESHOLD = 0.42
TIME_DELAY_BETWEEN_ALERTS = 5  # 5 seconds delay between alerts
LAST_ALERT_TIME = 0

def send_gmail_alert(subject, body, attachment_path=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_CONFIG['sender_email']
    msg['To'] = EMAIL_CONFIG['recipient_email']
    msg.set_content(body)

    if attachment_path:
        if not os.path.exists(attachment_path):
            print(f"Attachment file not found: {attachment_path}")
            return
            
        try:
            with open(attachment_path, 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                msg.add_attachment(
                    file_data,
                    maintype='image',
                    subtype='jpeg',
                    filename=file_name
                )
                print(f"Attached image: {file_name}")
        except Exception as e:
            print(f"Error attaching image: {e}")
            return

    try:
        with smtplib.SMTP_SSL(
            EMAIL_CONFIG['smtp_server'], 
            EMAIL_CONFIG['smtp_port']
        ) as server:
            server.login(
                EMAIL_CONFIG['sender_email'], 
                EMAIL_CONFIG['sender_password']
            )
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encodeList.append(encodings[0])
        else:
            print("No faces found in image.")
    return encodeList

def mark(name, markedNames):
    if name not in markedNames:
        with open(r'F:\GIT_HUB\HACKATHON\SMART_TRACKING_SYSTEM\att.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]

            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%Y-%m-%d %H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                markedNames.add(name)
                print(f" marked for {name} at {dtString}")
            else:
                print(f" already marked for {name}")
    else:
        print(f" already marked for {name}")

def saveUnknownFace(faceImg):
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    filename = os.path.join(unknown_faces_path, f"Unknown_{timestamp}.jpg")
    
    # Ensure directory exists
    if not os.path.exists(unknown_faces_path):
        os.makedirs(unknown_faces_path)
    
    # Check if image is valid
    if faceImg.size == 0:
        print("Empty image, not saving")
        return None
    
    cv2.imwrite(filename, faceImg)
    print(f"Unknown face saved as {filename}")
    return filename

encodeListKnown = findEncodings(images)
print("Encoding Done")

markedNames = set()
known_unknown_encodings = [] 
frame_counter = 0

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    frame_counter += 1
    if frame_counter % PROCESS_EVERY_N_FRAMES != 0:
        continue

    # Convert and resize frame
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect faces
    facesCurFrame = face_recognition.face_locations(imgS, model='hog')
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < DETECTION_THRESHOLD:
            name = classNames[matchIndex].upper()
            mark(name, markedNames)
            color = (0, 255, 0)
        else:
            name = 'Unknown'
            color = (0, 0, 255)
            
            # Process only if enough time has passed since last alert
            current_time = time.time()
            if current_time - LAST_ALERT_TIME < TIME_DELAY_BETWEEN_ALERTS:
                continue
            
            # Scale back up face locations
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            
            # Validate coordinates
            if y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0] or x1 < 0:
                print("Invalid face coordinates")
                continue
            
            faceImg = img[y1:y2, x1:x2].copy()
            
            # Process face image
            faceImgRGB = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB)
            unknown_encoding = face_recognition.face_encodings(faceImgRGB)
            
            if not unknown_encoding:
                print("No face found in cropped image")
                continue
            
            unknown_encoding = unknown_encoding[0]
            
            # Check for duplicates with time-based reset
            duplicate = any(
                face_recognition.compare_faces(
                    known_unknown_encodings,
                    unknown_encoding,
                    tolerance=0.4
                )
            )
            
            if not duplicate:
                filename = saveUnknownFace(faceImg)
                if filename:
                    known_unknown_encodings.append(unknown_encoding)
                    # Keep only recent 5 unknown faces
                    if len(known_unknown_encodings) > 5:
                        known_unknown_encodings.pop(0)
                    
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    send_gmail_alert(
                        f'🚨 Alert: Unknown Face @ {timestamp}',
                        f'Detected unknown face at {timestamp}\nFilename: {os.path.basename(filename)}',
                        filename
                    )
                    LAST_ALERT_TIME = current_time
            else:
                print("Duplicate unknown face detected, skipping")

        # Draw rectangle with name
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size = cv2.getTextSize(name, font, font_scale, thickness)[0]
        text_width, text_height = text_size

        cv2.putText(img, name, (x1 + (x2 - x1 - text_width) // 2, y2 - 10), 
                   font, font_scale, (255, 255, 255), thickness)

    cv2.imshow('Webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()