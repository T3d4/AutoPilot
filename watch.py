import os
import shutil
import time
import sys
import signal
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

homeDir = os.path.expanduser('~')
downloadDir = os.path.join(homeDir, "Downloads")
filenames = os.listdir(downloadDir)
musicDir = os.path.join(homeDir, "Music/")
documentDir = os.path.join(homeDir, "Documents/")
videoDir = os.path.join(homeDir, "Videos/")
programDir = os.path.join(homeDir, "Downloads/Programs/")
compressedDir = os.path.join(homeDir, "Downloads/Compressed/")
picDir = os.path.join(homeDir, "Pictures/")

observer = Observer()
monitoredDirectory = downloadDir

def moveFile(file):

    try:
        
        if file.endswith(".zip") | file.endswith(".tar.gz"):
            dstDirectory = documentDir
            shutil.move(file, dstDirectory)
            print(f"---{file} moved to '{dstDirectory}'---")
        
        elif file.endswith(".jpg") | file.endswith(".png"):
            dstDirectory = picDir
            shutil.move(file, dstDirectory)
            print(f"---{file} moved to '{dstDirectory}'---")
        
        elif file.endswith(".mkv") | file.endswith(".mp4"):
            dstDirectory = videoDir
            shutil.move(file, dstDirectory)
            print(f"---{file} moved to '{dstDirectory}'---")
        
    except FileNotFoundError as e:
         print(f"Destination directory does not exist: {e}")
         os.makedirs(dstDirectory)
         print(f"---{dstDirectory} created---")
         moveFile(file, dstDirectory)

    except shutil.Error as e:
         print(f"---{e}---")

class DirectoryListener(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent):
        if event.is_directory:
            return None
        
        if event.src_path.endswith(".mkv.crdownload"):
            return
        
        print(f"File Modified: {event.src_path}")
        
        moveFile(event.src_path)        

eventHandler = DirectoryListener()

def signalHandler(sig, frame):
    if sig == signal.SIGINT:
        print("\nRecieved Ctrl+C, stopping observer...")
    if sig == signal.SIGTERM:
        print("\nRecieved SIGTERM, stopping observer...")
    
    observer.stop()
    observer.join()
    sys.exit(0)


def moveHandler(eventHandler, observer, path):
     
    try:
        observer.schedule(eventHandler, path, recursive=True)
        observer.start()
         
    except RuntimeError as e:
         print(f"---{e}---")

def watchDog():

    for filename in filenames:
        filename = os.path.join(downloadDir, filename)
        moveFile(filename)

    moveHandler(eventHandler, observer, monitoredDirectory)

    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)

    try: 
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        return

watchDog()