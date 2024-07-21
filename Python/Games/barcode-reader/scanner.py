import cv2
import math
import time
from pyzbar.pyzbar import decode
from playsound import playsound
from loguru import logger
from basket import Basket, StockControl
from loyalty import LoyaltyMember, LoyaltyScheme


# Camera parameters
cam = cv2.VideoCapture(1)
alpha = 1.0  # Contrast control (1.0-3.0)
beta = 20  # Brightness control (0-100)

# Loyalty card members
members = [
    LoyaltyMember("Reuben", b"Reuben", 100),
    LoyaltyMember("Peter", b"Peter", 100),
    LoyaltyMember("Kiki", b"Birdcatcher", 100),
]
loyalty_scheme = LoyaltyScheme(members)

# Beep sound
beep_sound = "beep.wav"

# Font
font = cv2.FONT_HERSHEY_SIMPLEX

# Basket to hold items
basket = Basket()

# Stock control component
stock_control = StockControl(199)

# Last time (in seconds) that a scan occurred
last_scan_time = None


def add_banner(frame):
    h, w, c = frame.shape
    cv2.rectangle(frame, (0, 0), (w, 80), (170, 80, 0), -1)
    cv2.rectangle(frame, (10, 10), (w - 10, 70), (20, 10, 230), 5)
    cv2.putText(frame, "Supermarket", (30, 50), font, 1, (0, 240, 255), 2, cv2.LINE_AA)

    margin = 4
    cv2.rectangle(frame, (0, 0), (margin, h), (170, 80, 0), -1)
    cv2.rectangle(frame, (w - margin, 0), (w, h), (170, 80, 0), -1)


def format_pence(pence: int):
    """Format the price (in pence) for the screen."""
    assert type(pence) == int

    num_pounds = math.floor(pence / 100)
    num_pence = pence - 100 * num_pounds
    return f"${num_pounds}.{num_pence:02d}"


def add_main_display(frame, basket: Basket):
    h, w, c = frame.shape
    bar_height = 200
    cv2.rectangle(frame, (0, h - bar_height), (w, h), (170, 80, 0), -1)

    if basket.is_empty():
        cv2.putText(
            frame,
            "Please scan an item",
            (10, h - 140),
            font,
            2,
            (0, 240, 255),
            2,
            cv2.LINE_AA,
        )
    else:
        cv2.putText(
            frame,
            format_pence(basket.last_item_cost()),
            (10, h - 150),
            font,
            2,
            (0, 240, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.putText(
            frame,
            "Total: " + format_pence(basket.total_cost()),
            (10, h - 80),
            font,
            2,
            (0, 240, 255),
            2,
            cv2.LINE_AA,
        )

    if basket.loyalty_member is not None:
        msg = (
            basket.loyalty_member.name
            + "'s points: "
            + str(basket.loyalty_member.points)
        )
        cv2.putText(frame, msg, (10, h - 15), font, 2, (0, 240, 255), 2, cv2.LINE_AA)


def read_barcode(frame) -> bytes | None:
    detected_barcodes = decode(frame)

    if len(detected_barcodes) == 0:
        return None
    else:
        barcode = detected_barcodes[0]
        logger.info(f"Detected barcode: {barcode.data}, type: {barcode.type}")
        return barcode


def barcode_detected(
    barcode: bytes,
    loyalty_scheme: LoyaltyScheme,
    basket: Basket,
    stock_control: StockControl,
):

    # Does the barcode belong to a loyalty card member?
    member = loyalty_scheme.get_member(barcode)

    if member is not None:
        logger.info(f"Detected barcode is for member: {member.name}")
        basket.add_loyalty(member)
        return

    item = stock_control.lookup(barcode)
    logger.info(f"Detected barcode is for item: {item}")
    basket.add_item(item)


logger.info("Starting main loop")
while True:

    # Read a frame from the camera
    result, frame = cam.read()
    if not result:
        continue

    # Adjust brightness
    frame = cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

    # Should the basket be automatically cleared?
    if not basket.is_empty() and (time.time() - last_scan_time > 15):
        logger.info("Clearing basket")
        basket = Basket()
        last_basket_update = None

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
        barcode_detected(barcode.data, loyalty_scheme, basket, stock_control)
        last_scan_time = time.time()

    # Resize the frame to make it easier to see on the screen
    frame = cv2.resize(frame, None, fx=2, fy=2)
    frame = cv2.flip(frame, 1)

    # Add the banner to the frame and the main display
    add_banner(frame)
    add_main_display(frame, basket)

    # Display the frame
    cv2.imshow("Scanner", frame)
    cv2.waitKey(5)
