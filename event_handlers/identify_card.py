import pytesseract
import time
import os
from watchdog.events import FileSystemEventHandler
from helpers.process_text import CleanText
from helpers.identify_pan_card import IdentifyPanCard

class IdentifyCard(FileSystemEventHandler):
    def on_created(self, event):
        # Get image path
        image_path = event.src_path

        # Get file name
        image_file_name = os.path.basename(image_path)

        # Pan card Pattern1 path
        pan_card_p1_path = os.path.join(r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\pan_card\pattern1', image_file_name)

        # Pan card Pattern2 path
        pan_card_p2_path = os.path.join(r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\pan_card\pattern2', image_file_name)

        # Wait for 1 second before reading the file
        time.sleep(1)

        # Configure tesseract
        tesseract_config = r'-l eng --oem 3 --psm 6'

        # Get the text in Dict from image
        data_text = pytesseract.image_to_string(image_path, output_type=pytesseract.Output.DICT,config=tesseract_config)
        clean_text = CleanText(data_text).clean_text()

        # Check for Pan card
        pan_card = IdentifyPanCard(clean_text)
        if pan_card.check_pan_card():
            if pan_card.identify_pan_card_pattern_1():
                os.rename(image_path, pan_card_p1_path)
            else:
                os.rename(image_path, pan_card_p2_path)
