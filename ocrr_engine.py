import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from event_handlers.validate_jpeg_image import JPEGEventHandler
from event_handlers.identify_card import IdentifyCard

# async func: monitor the folder for newly copied images
async def monitor_upload():
    # Create observer object
    observer = Observer()

    # Create custom event handler for validating JPEG image format
    validate_jpeg_event_handler = JPEGEventHandler()

    # Create scheduler for 'validate_jpeg_event_handler'
    observer.schedule(validate_jpeg_event_handler, monitor_path, recursive=True)

    # Create scheduler for 
    observer.start()

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

# async func: monitor the processed images
async def monitor_processed_images():
    # Create observer object
    observer = Observer()

    # Create custom event handler for identifying Pan or Aadhaar card
    identify_card_event_handler = IdentifyCard()

    # Create scheduler for 'identify_card_event_handler'
    observer.schedule(identify_card_event_handler, monitor_processed_image_path, recursive=True)

    # Create scheduler for 
    observer.start()

    try:
        while True:
            await asyncio.sleep(3)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


# async func: main
async def main():
    task1 = asyncio.create_task(monitor_upload())
    task2 = asyncio.create_task(monitor_processed_images())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':

    # Directory to monitor for JPEG files
    monitor_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\upload'
 
    # Directory to monitor processed images
    monitor_processed_image_path = r'C:\Users\pokhriyal\Desktop\OCRR-Engine\images\processed_images'

    # Run main
    asyncio.run(main())
