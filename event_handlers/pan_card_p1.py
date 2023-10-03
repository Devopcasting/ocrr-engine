import os
import shutil
from watchdog.events import FileSystemEventHandler
from pancard.pattern1 import PanCardPatteern1
from helpers.write_xml import WriteXML
from ocrr_logging.ocrr_engine_log import OCRREngineLogging

class PanCardPattern1Handler(FileSystemEventHandler):
    def on_created(self, event):
         # Configure logger
        config = OCRREngineLogging()
        logger = config.configure_logger()

        # Get the image path
        self.image_path = event.src_path

        # Get the image name
        image_file_name = os.path.basename(self.image_path)

        # Get the rejcted image path
        rejected_image_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\rejected_images'

        # Get the finished path
        finished_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\finished'

        # Get xml file path
        xmls_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\xmls'

        # Collect pan card informations
        collect_pan_card_info_obj = PanCardPatteern1(self.image_path).collect_pan_card_info()

        if collect_pan_card_info_obj:
            WriteXML(xmls_path, image_file_name, collect_pan_card_info_obj ).writexml()
            logger.info(f"Writing XML file")

            # Move the image to finished folder
            shutil.move(self.image_path,  os.path.join(finished_path, image_file_name))
            logger.info(f"Pan card moved to finished folder")         
        else:
            # Move the image to rejected folder
            shutil.move(self.image_path,  os.path.join(rejected_image_path, image_file_name))
            logger.error(f"Pan card {image_file_name} is rejected and moved to rejected folder") 