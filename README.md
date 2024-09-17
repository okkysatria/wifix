# Wi-Fi Password Viewer for Windows

A simple application to display and save SSID and passwords of Wi-Fi networks saved on your Windows machine. The application provides both an executable file and a Python script for usage.
<div align="center">
  <img src="https://github.com/user-attachments/assets/a51473c6-1003-4a2d-a95b-7177a6482741" alt="ss" width="500"/>
</div>


## Requirements

- Windows 10/11
- [Python 3.11.x](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe) (for using the Python script, not required for the executable)

## Download and Installation

### Option 1: Using the Executable

1. **Download the Executable:**
   - [Download](https://github.com/okkysatria/wifix/releases/download/v1/wifix.exe)

2. **Run the Executable:**
   - Double-click `wifix.exe` to launch the application. It will scan and display saved Wi-Fi profiles along with their passwords.
   - Use the buttons in the GUI to perform actions:
     - **Rescan:** Starts a new scan for Wi-Fi profiles.
     - **Save to Note:** Saves the displayed Wi-Fi data to a file.
     - **Search:** Searches for a specific Wi-Fi profile by name.

### Option 2: Using the Python Script

1. **Download the Repository:**
   - [Download ZIP](https://github.com/okkysatria/wifix/archive/refs/heads/main.zip)

2. **Extract the ZIP File:**
   - Extract the downloaded ZIP file to a desired location on your computer.

3. **Install Python:**
   - Ensure Python 3.11.x is installed on your system. Download it from the [official Python website](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe).

4. **Install Dependencies:**
   - Open a command prompt or terminal and navigate to the extracted directory. Install the required Python libraries using pip:
     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Script:**
   - Double-click `wifi_profiles.py` to execute the script.

6. **Interactive Commands:**
   - Press `e` to exit the script.
   - Press `s` to save SSID and passwords.

7. **Save File Path:**
   - After pressing `s`, provide a file path where the SSID and passwords will be saved.
   - Example file path: `C:\Users\yourusername\Downloads\filename.txt`
   - Replace `yourusername` with your actual username and `filename.txt` with your desired file name.
