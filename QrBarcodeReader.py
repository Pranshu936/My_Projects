import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
import webbrowser

data_file_path = 'myDataFile.text'
if not os.path.exists(data_file_path):
    with open(data_file_path, 'w') as f:
        f.write('')

def process_frame(img):
    for barcode in decode(img):
        myData = barcode.data.decode('utf-8')
        print("Detected Data:", myData)

        if myData.startswith(('http://', 'https://')):
            print("Opening URL:", myData)
            webbrowser.open(myData)
        else:
            print("Storing text data in file.")
            with open(data_file_path, 'a') as f:
                f.write(myData + '\n')

        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(img, [pts], True, (255, 0, 0), 5)
        pts2 = barcode.rect
        cv2.putText(img, myData, (pts2[0], pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    return img

choice = input("Do you want to use a static image or the webcam? Enter 'image' or 'webcam': ").strip().lower()

if choice == 'image':
    image_path = input("Enter the path to the image file: ").strip()
    if os.path.exists(image_path):
        img = cv2.imread(image_path)
        img = process_frame(img)
        cv2.imshow('Result', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print(f"Image file '{image_path}' not found.")
elif choice == 'webcam':
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        success, img = cap.read()
        if not success:
            break

        img = process_frame(img)
        cv2.imshow('Result', img)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
else:
    print("Invalid input. Please restart the program and enter 'image' or 'webcam'.")
