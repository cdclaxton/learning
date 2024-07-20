import cv2
import math
import time
from pyzbar.pyzbar import decode 
from playsound import playsound

cam = cv2.VideoCapture(1)

last_detection = None
last_time = None
last_cost = None  # in pence
total = 0

beep_sound = "beep.wav"    
font = cv2.FONT_HERSHEY_SIMPLEX

def cost_in_pence_from_barcode(barcode):

    # Decode the barcode
    d = barcode.data.decode('utf-8')

    # Extract the required digits
    return 100 * int(d[-3]) + 10 * int(d[-2]) + int(d[-1])

def format_pence(pence):

    num_pounds = math.floor(pence / 100)
    num_pence = pence - 100 * num_pounds
    return f"${num_pounds}.{num_pence:02d}"


while True:
    result, frame = cam.read()

    if last_detection is not None and (time.time() - last_time > 10):
        last_detection = None
        last_time = None
        last_cost = None
        total = 0

    if not result:
        continue

    alpha = 1.0 # Contrast control (1.0-3.0)
    beta = 10 # Brightness control (0-100)
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Decode the barcode image 
    detected_barcodes = decode(frame) 
       
    # If not detected then print the message 
    if len(detected_barcodes) > 0:

        barcode = detected_barcodes[0]

        # Locate the barcode position in image 
        (x, y, w, h) = barcode.rect 

        # Add a bounding box to the barcode
        cv2.rectangle(frame, (x-10, y-10), 
                        (x + w+10, y + h+10),  
                        (255, 0, 0), 2)

        # Store the detection and play a beep if it's a 'new' detection
        current_time = time.time()
        if last_detection is None or (current_time - last_time) > 2:
            last_detection = barcode.data
            last_time = current_time

            # Extract the 'cost' from the barcode
            last_cost = cost_in_pence_from_barcode(barcode)
            total += last_cost            

            playsound(beep_sound) 
            print(f"Barcode: {barcode.data}, type: {barcode.type}") 

    # Resize the frame to make it easier to see on the screen
    frame = cv2.resize(frame, None, fx=2, fy=2)
    frame = cv2.flip(frame, 1)

    h, w, c = frame.shape

    cv2.rectangle(frame, (0,0), (w, 80), (170, 80, 0), -1)
    cv2.rectangle(frame, (10, 10), (w-10, 70), (20, 10, 230), 5)
    cv2.putText(frame, "Peter's Supermarket", (30,50), font, 1, (0, 240, 255), 2, cv2.LINE_AA)

    bar_height = 200
    cv2.rectangle(frame, (0,h-bar_height), (w, h), (170, 80, 0), -1)

    if last_cost is not None:
        cv2.putText(frame, format_pence(last_cost), (10,h - 140), font, 2, (0, 240, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "Total = " + format_pence(total), (10,h-60), font, 2, (0, 240, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(frame, "Please scan an item", (10,h - 140), font, 2, (0, 240, 255), 2, cv2.LINE_AA)

    cv2.imshow("Frame", frame)
    cv2.waitKey(5)