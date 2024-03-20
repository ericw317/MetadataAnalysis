import os
import datetime
from datetime import datetime
from datetime import timedelta
import tkinter
from tkinter import filedialog
from tkinter import messagebox

root = tkinter.Tk()
root.wm_attributes("-topmost", 1)
root.withdraw()

def print_metadata(file):
    if (os.path.getsize(file)) < 1000:
        unit = "b"
        division = 1
    elif 1000 < (os.path.getsize(file)) < 1000000:
        unit = "kb"
        division = 1000
    elif 1000000 < (os.path.getsize(file)) < 1000000000:
        unit = "mb"
        division = 1000000
    elif 1000000000 < (os.path.getsize(file)):
        unit = "gb"
        division = 1000000000
    else:
        division = 0
        unit = ""

    return "Name: " + file + "\n" + "Creation Date: " + str(datetime.fromtimestamp(os.path.getctime(file))) + "\n" \
           "Modification Date: " + str(datetime.fromtimestamp(os.path.getmtime(file))) + "\n" \
           "Size: " + str(os.path.getsize(file) / division) + unit + "\n\n\n"

def write_to_file(data):
    fi = open(path + "/report.txt", "a")
    fi.write(data)
    fi.close()


messagebox.showinfo("Selection", "Select a directory to search through.")
path = filedialog.askdirectory()
all_files = os.listdir(path)  # store names of all files in chosen directory
current_date = datetime.now()  # store the current date and time
delta = timedelta(hours=24)  # time used for subtraction later on
upper_threshold = 1000000000
lower_threshold = 10000
# list of suspicious keywords
suspicious_keywords = ["virus", "malware", "trojan", "phishing", "exploit", "ransomware", "spyware", "keylogger"
                       "backdoor", "rootkit", "botnet", "worm", ".exe", ".bat", ".vbs", ".js", ".jar", ".ps1",
                       ".scr", ".dll", ".com", ".pif", ".cmd", ".zip"]

# go through every file in the directory
for file in all_files:
    path_reference = os.path.join(path, file)

    file_creation_date = datetime.fromtimestamp(os.path.getctime(path_reference))  # store file creation date
    file_modification_date = datetime.fromtimestamp(os.path.getmtime(path_reference))  # store file modification date
    # check if file was created within 24 hours of current date
    if file_creation_date > current_date - delta or file_modification_date > current_date - delta:
        print(print_metadata(file))
        write_to_file(print_metadata(file))
    elif os.path.getsize(path_reference) < lower_threshold or os.path.getsize(path_reference) > upper_threshold:
        print(print_metadata(path_reference))
        write_to_file(print_metadata(path_reference))
    else:
        # search for suspicious keywords
        for keyword in suspicious_keywords:
            if keyword in file:
                print(print_metadata(file))
                write_to_file(print_metadata(file))

if os.path.exists(path + "/report.txt"):
    os.startfile(path + "/report.txt")
