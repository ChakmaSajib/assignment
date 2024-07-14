import os
import time
from ftplib import FTP
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import xml.etree.ElementTree as ET

FTP_SERVER = 'localhost'
FTP_USER = 'nybsys'
FTP_PASSWORD = '12345'
TEMP_FOLDER = 'temp'
LOCAL_FOLDER = 'local'
TRASH_FOLDER = 'trash'


# To create directory
def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError as error:
        print(f"Error creating directory {directory}: {error}")
        raise


def download_xml_files_and_store_in_temp_folder():
    """
    1. Download newly uploaded xml file from the FTP server, then 
    2. Store in TEMP folder while download is finished
    3. Finally, move file into a Local folder when download is finished
    """
    
    # Create 'temp' and 'local' folder if they don't exists
    create_directory(TEMP_FOLDER)
    create_directory(LOCAL_FOLDER)
    
    # Connect FTP server then check file and store 
    ftp_server = FTP(FTP_SERVER) 
    ftp_server.login(FTP_USER, FTP_PASSWORD)
    ftp_server.cwd('/')
    
    filenames = ftp_server.nlst()
    
    try:
        for filename in filenames:
            temp_path = os.path.join(TEMP_FOLDER, filename)
            local_path = os.path.join(LOCAL_FOLDER, filename)
            
            if not os.path.exists(temp_path):
                with open(temp_path, 'wb') as file:
                    ftp_server.retrbinary('RETR ' + filename, file.write)
                # Move the file to the local folder
                os.rename(temp_path, local_path)
    except Exception as error:
        print(f"An error occurred: {error}")
    
    finally:
        ftp_server.quit()


class FileHandler(FileSystemEventHandler):
    """
    Monitor continously the local folder for any new files being moved into it or not
    """
    def on_created(self, event):
        if event.is_directory:
            return
        process_file(event.src_path)


def monitor_local_folder():
    file_event_handler = FileHandler()
    observer = Observer()
    observer.schedule(file_event_handler, path=LOCAL_FOLDER, recursive=False)
    observer.start()
    print(f"New file added in local folder. \n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


def process_file(file_path):
    """
    1. Detect new XML files in the local folder.
    2. Extract values and parameter names from xml file, converting them to a dictionary.
    3. Print the dictionary.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    
        data_dict = {}
        
        for element in root.iter():
            for attr, value in element.attrib.items():
                if not attr.startswith('{'):
                    if attr in data_dict:
                        if isinstance(data_dict[attr], list):
                            data_dict[attr].append(value)
                        else:
                            data_dict[attr] = [data_dict[attr], value]
                    else:
                        data_dict[attr] = value        
        print(f"Process file: {file_path} \n")
        print(data_dict)
        
        # Move the files to a trash folder for later observation
        move_to_trash_folder(file_path)

    except ET.ParseError as error:
        print(f"Error parsing XML file {file_path}: {error}")
    

# Move to trash folder
def move_to_trash_folder(file_path):
    create_directory(TRASH_FOLDER)

    try:
        file_name = os.path.basename(file_path)
        trash_path = os.path.join(TRASH_FOLDER, file_name)
        os.rename(file_path, trash_path)
        print(f"\n Moved {file_name} to {TRASH_FOLDER}")
    except OSError as error:
        print(f"Error moving file {file_path} to trash: {error}")


def main():
    download_xml_files_and_store_in_temp_folder()
    
    # Monitor the local folder for new file
    monitor_local_folder()
    

if __name__=='__main__':
   main()
