# 2024 July 5 
# Filename: data_manager.py
# Use: Store the data that are coming through 

from collections import defaultdict
import pandas as pd 
import json 
import os 

# Get folder path
base_path = os.getcwd() + "/bowen_clinic"

class ClinicStorage:
    def __init__(self):
        # File directory
        self.Json_File_Path = os.path.join(base_path, 'Json Storage')
        self.CSV_File_Path = os.path.join(base_path, 'CSV Storage')

    def load_json(self, filename):
        try:
            json_file_path = os.path.join(self.Json_File_Path, filename)
            with open(json_file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return defaultdict(list)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {filename}")
            return defaultdict(list)
        
    def save_csv(self, data: dict, filename):
        print(f"Saving {filename}...") 
        csv_file_path = os.path.join(self.CSV_File_Path, filename)
        data = pd.DataFrame(data)
        data.to_csv(csv_file_path, header=True, index=False)

    def save_json(self, data: dict, filename):
        print(f"Saving {filename}...") 
        try:
            json_file_path = os.path.join(self.Json_File_Path, filename)
            with open(json_file_path, 'w') as file:
                json.dump(data, file, indent=4, ensure_ascii=False) # store data
        except IOError as e:
            print(f"Error writing to {filename}: {e}")
       
    def modify_system_log(self, action: list):
        # Add message when new action is done
        # action = [doctor_id, time, modified_filename] 
        file = os.path.join(self.Json_File_Path, "system_log.txt")
        file = open(file, "a")
        file.write(action)
        file.write('\n') # new line 
        file.close() 


clinic_storage = ClinicStorage() 