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

observer = Observer()
monitoredDirectory = downloadDir

def moveFile(source, file):

    try:
        directory = os.path.join(source, file)
        dstDirectory = programDir
        if file.endswith(".zip"):
            shutil.move(directory, dstDirectory)
            print(f"---{file} moved to {dstDirectory}---")
        else:
            return
        
    except FileNotFoundError as e:
         print(f"Destination directory does not exist: {e}")
         os.makedirs(programDir)
         print(f"{programDir} ---Created---")
         moveFile(source, file)

    except shutil.Error as e:
         print(f"---{e}---")

class DirectoryListener(FileSystemEventHandler):
     def on_modified(self, event: FileSystemEvent):
          if event.is_directory:
               return None
          
          observer.schedule(moveFile, downloadDir, event.src_path, recursive=True)

          print(f"File Modified ---{event.src_path}---")


eventHandler = DirectoryListener()

def signalHandler(sig, frame):
    if sig == signal.SIGINT:
        print("Recieved Ctrl+C, stopping observer...")
    if sig == signal.SIGTERM:
        print("Recieved SIGTERM, stopping observer...")
    else:
        print(f"Recieved unknown signal {sig}, ignoring...") 
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
    signal.signal(signal.SIGINT, signalHandler)
    signal.signal(signal.SIGTERM, signalHandler)

    moveHandler(eventHandler, observer, monitoredDirectory)

    try: 
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        return

watchDog()