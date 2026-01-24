import cv2
import time
from pyzbar.pyzbar import decode
from playsound import playsound
from loguru import logger


# Camera parameters
cam = cv2.VideoCapture(1)
alpha = 2.0  # Contrast control (1.0-3.0)
beta = 100  # Brightness control (0-100)

# Beep sound
beep_sound = "beep.wav"

# Font
font = cv2.FONT_HERSHEY_SIMPLEX

# Last time (in seconds) that a scan occurred
last_scan_time = None

detected_barcodes_filepath = "barcodes.txt"
seen_barcodes = set()


def read_barcode(frame) -> bytes | None:
    detected_barcodes = decode(frame)

    if len(detected_barcodes) == 0:
        return None
    else:
        barcode = detected_barcodes[0]
        logger.info(f"Detected barcode: {barcode.data}, type: {barcode.type}")
        return barcode


logger.info("Starting main loop")
while True:

    # Read a frame from the camera
    result, frame = cam.read()
    if not result:
        continue

    # Adjust brightness
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Detect a barcode in the frame
    barcode = read_barcode(frame)
    if barcode is not None:
        # Locate the barcode position in image
        (x, y, w, h) = barcode.rect

        # Add a bounding box to the barcode
        cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), (255, 0, 0), 2)

    if barcode is not None and (
        last_scan_time is None or (time.time() - last_scan_time) > 2
    ):
        playsound(beep_sound)
        last_scan_time = time.time()
        print(barcode)
        b = barcode.data.decode("utf-8")
        if b not in seen_barcodes:
            with open(detected_barcodes_filepath, "a+") as fp:
                fp.write(b + "\n")
            seen_barcodes.add(b)

    # Resize the frame to make it easier to see on the screen
    frame = cv2.resize(frame, None, fx=2, fy=2)
    frame = cv2.flip(frame, 1)

    # Display the frame
    cv2.imshow("Scanner", frame)
    cv2.waitKey(5)
