import os
import time
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- CONFIGURATION ---
# Change this to the folder you want to monitor
FOLDER_TO_WATCH = r"C:/Users/abdul/Documents/GitHub/IPMC-LDP_Newsletter/02_delegates" 

class PrefixRenameHandler(FileSystemEventHandler):
    def on_created(self, event):
        # Ignore directories
        if event.is_directory:
            return

        # Brief pause to let the OS finish copying the file
        time.sleep(1)

        old_filepath = event.src_path
        directory = os.path.dirname(old_filepath)
        filename = os.path.basename(old_filepath)

        # Check if the file already starts with a number and an underscore (e.g., "01_")
        # This prevents the script from accidentally adding another prefix to a file it just renamed!
        if re.match(r"^\d+_", filename):
            return

        # Figure out the next number in the sequence
        next_num = 1
        existing_files = os.listdir(directory)
        for f in existing_files:
            # Look for existing files that start with numbers followed by an underscore
            match = re.match(r"^(\d+)_", f)
            if match:
                # Extract the number and check if it's the highest one so far
                num = int(match.group(1))
                if num >= next_num:
                    next_num = num + 1

        # Format the new number with a leading zero (e.g., 1 becomes "01_", 10 becomes "10_")
        # If you want three digits (e.g., "001_"), change :02d to :03d
        prefix = f"{next_num:02d}_"
        
        # Combine the new prefix with the original filename
        new_filename = f"{prefix}{filename}"
        new_filepath = os.path.join(directory, new_filename)

        # Rename the file
        try:
            os.rename(old_filepath, new_filepath)
            print(f"Success: Added prefix -> '{new_filename}'")
        except Exception as e:
            print(f"Error renaming '{filename}': {e}")

# --- START THE WATCHER ---
if __name__ == "__main__":
    if not os.path.exists(FOLDER_TO_WATCH):
        print(f"Error: The folder {FOLDER_TO_WATCH} does not exist.")
    else:
        event_handler = PrefixRenameHandler()
        observer = Observer()
        observer.schedule(event_handler, FOLDER_TO_WATCH, recursive=False)
        observer.start()
        print(f"Watching folder: {FOLDER_TO_WATCH}")
        print("Waiting for new files... (Press Ctrl+C to stop)")
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            print("\nStopped watching.")
        
        observer.join()