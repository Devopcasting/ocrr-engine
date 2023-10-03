import pytesseract
import time
import os
import shutil
from watchdog.events import FileSystemEventHandler
from helpers.process_text import CleanText
from helpers.identify_pan_card import IdentifyPanCard
from ocrr_logging.ocrr_engine_log import OCRREngineLogging

class IdentifyCard(FileSystemEventHandler):
    def on_created(self, event):
        # Configure logger
        config = OCRREngineLogging()
        logger = config.configure_logger()

        # Get image path
        image_path = event.src_path

        # Get file name
        image_file_name = os.path.basename(image_path)

        # Pan card Pattern1 path
        pan_card_p1_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\pan_card\pattern1'

        # Pan card Pattern2 path
        pan_card_p2_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\pan_card\pattern2'

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
                logger.info(f"Move image to Pan card Pattern-1 folder")
                shutil.move(image_path, os.path.join(pan_card_p1_path, image_file_name))
            else:
                logger.info(f"Move image to Pan card Pattern-2 folder")
                shutil.move(image_path, os.path.join(pan_card_p2_path, image_file_name))
