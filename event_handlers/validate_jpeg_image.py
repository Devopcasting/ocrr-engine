import magic
import time
import shutil
import os
from watchdog.events import FileSystemEventHandler
from ocrr_logging.ocrr_engine_log import OCRREngineLogging
from helpers.process_image import ProcessJPEGImages

class JPEGEventHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Configure logger
        config = OCRREngineLogging()
        logger = config.configure_logger()

        # Get image path
        image_path = event.src_path

        # Get filename
        file_name = os.path.basename(image_path)

        # Set Invalid image path
        invalid_image_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\invalid_images'

        # Wait for 1 second before reading the file
        time.sleep(1)

        # Set the process image path
        process_image_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\processed_images'

        # Set image magic
        image_mime = magic.Magic()
        image_format = image_mime.from_file(image_path)

        # Check if the image is valid JPEG
        if image_format.split(" ")[0] in ["JPEG", "JPG"]:
            logger.info(f"Valid JPEG image at {image_path}")
            if ProcessJPEGImages(image_path, process_image_path).processed_image():
                logger.info(f"Processed JPEG image at {process_image_path}")
            else:
                logger.error(f"Error while processing image")
                shutil.move(image_path, os.path.join(invalid_image_path, file_name))
        else:
            logger.error(f"Not a valid JPEG image at {image_path}")
            shutil.move(image_path, os.path.join(invalid_image_path, file_name))