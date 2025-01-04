import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import requests

path = r'F:\GIT_HUB\HACKATHON\SMART_TRACKING_SYSTEM\IMAGES_KNOWN'
unknown_faces_path = r'F:\GIT_HUB\HACKATHON\SMART_TRACKING_SYSTEM\IMAGES_UNKNOWN'
images = []
classNames = []
myList = os.listdir(path)
print(f"Images found: {myList}")

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(f"Class names: {classNames}")

def send_email_alert_mailbluster(to_email, subject, body):
    API_KEY = 'e313cf59-d85d-4d29-9b00-cad3af9576c5' 
    API_URL = 'https://app.mailbluster.com/K37jeedQEg'
    
    email_data = {
        'from': 'priyanshuraikwar2305@gmail.com', 
        'to': to_email,  
        'subject': subject, 
        'body': body,  
        'is_html': False  
    }

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(API_URL, json=email_data, headers=headers)
        if response.status_code == 200:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            print(response.json())
    except Exception as e:
        print(f"An error occurred: {e}")

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
    filename = f'{unknown_faces_path}\\Unknown_{timestamp}.jpg'
    cv2.imwrite(filename, faceImg)
    print(f"Unknown face saved as {filename}")

encodeListKnown = findEncodings(images)
print("Encoding Done")

markedNames = set()
known_unknown_encodings = [] 

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS, model='hog')
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.42:
            name = classNames[matchIndex].upper()
            mark(name, markedNames)
            color = (0, 255, 0)
        else:
            name = 'Unknown'
            color = (0, 0, 255)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            faceImg = img[y1:y2, x1:x2]  
            faceImgRGB = cv2.cvtColor(faceImg, cv2.COLOR_BGR2RGB) 
            
            unknown_encoding = face_recognition.face_encodings(faceImgRGB)
            if unknown_encoding:
                unknown_encoding = unknown_encoding[0]
                if not any(face_recognition.compare_faces(known_unknown_encodings, unknown_encoding)):
                    saveUnknownFace(faceImg)  
                    known_unknown_encodings.append(unknown_encoding)  
                    send_email_alert_mailbluster( 
                        'vdubey8511@gmail.com',
                        'Alert: Unknown Face Detected',
                        f'An unknown face was detected at {datetime.now()}. Please check the webcam feed.'
                    )
                else:
                    print("Duplicate unknown face detected, not saving.")
            
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2
        text_size = cv2.getTextSize(name, font, font_scale, thickness)[0]
        text_width, text_height = text_size

        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), color, cv2.FILLED)
        cv2.putText(img, name, (x1 + (x2 - x1 - text_width) // 2, y2 - 10), font, font_scale, (255, 255, 255), thickness)

    cv2.imshow('Webcam', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()