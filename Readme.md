## Getting Started

### Step 1: Create Virtual Environment

Create a virtual environment inside folder to avoid conflicts with system-wide Python installations:
```bash
virtualenv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

### Step 2: Install Dependencies

Install `watchdog` package in the virtual environment:

```bash
pip3 install watchdog
```

### Step 3: Start FTP Server
To start the `FTP` server using `Docker` run:
```bash
make start
```

To down `Docker` container:
```bash
make stop
```

### Core function Explanation:
1. `Directory Creation`: The `create_directory` function ensures that necessary directories exist or are created. Here, we are creating `temp`, `local` and `trash` folder.

2. `Downloading Files from FTP`:
The `download_xml_files_and_store_in_temp_folder` function connects to the FTP server, downloads files to the `TEMP_FOLDER`, and then moves them to the `LOCAL_FOLDER`.

3. `Monitoring Local Folder`:
The `monitor_local_folder` function sets up a `watchdog` observer to monitor the `LOCAL_FOLDER` for new files.

4. `Processing Files`:
The `process_file function` parses each new XML file, extracts data into a dictionary, prints the dictionary, and moves the file to the `TRASH_FOLDER`.

5. `Moving Files to Trash`:
The `move_to_trash_folder` function moves processed files to the `TRASH_FOLDER`.

<br>

#### Workflow Brief:
I added `xml-sample-data` folder (where given xml files are located) in here, and we can use these xml file to check the script workflow. Here, we have `ftp` folder which is mounted with `/home/vsftpd/nybsys` and if we move/upload file in the `ftp` folder, that means we are uploading file into `FTP` server. Then, we can keep downloading new xml file from the server, then store in TEMP folder, again, then move file into Local folder and this Local folder will be monitored continuesly to figure out any new files being is added or not and so on.

`Noted`:
<br>
The "`value`" in XML can refer to two things (`Text Content` and `Attribute Value`) , since we need to extract parameter name and value, here in this script I took attribute value as value.
For example, in `<measType p="1">`, the value associated with the attribute `p` is `1`. 
