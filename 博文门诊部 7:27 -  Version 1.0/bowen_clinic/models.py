from . import clinic_storage_manager
from . import data_storage
from datetime import datetime

clinic_storage = clinic_storage_manager.ClinicStorage() 

def calculate_patient_age(birth_year: str) -> str:
    return str(int(datetime.now().strftime("%Y")) - int(birth_year)) + "岁"

###############################################################################################################################

class Doctor:
    def __init__(self, doctor_id, name, gender):
        self.doctor_id = doctor_id
        self.name = name 
        self.gender = gender 
        self.time = datetime.now().strftime("%Y-%m-%d")
    
    def __str__(self):
        return f"医生 - | 医生 ID: {self.medicine_id} | 名字: {self.name} | 性别: {self.gender} |"

    def add_new_doctor(self):
        clinic_storage.modify_system_log(f"新医生 - | {self.time:^20} | 医生 ID: {self.doctor_id:^5} | 名字: {self.name:^15} | 性别: {self.gender:^2} |")
        data_storage.doctor_storage.store_new_doctor(self.doctor_id, [self.name, self.gender, self.time])

    def delete_doctor(self, doctor_id):
        current_time = datetime.now().strftime("%Y-%m-%d")
        clinic_storage.modify_system_log(f"删除医生 - | {current_time:^20} | 医生 ID: {doctor_id:^5} |")
        data_storage.doctor_storage.delete_doctor(str(doctor_id), current_time)

###############################################################################################################################

class Patient:
    def __init__(self, patient_id, doctor_id, name, birth_year, gender, phone, medical_record):
        # Temporary Storage for patient attributes
        self.patient_id = patient_id
        self.doctor_id = doctor_id # Responsible doctor
        self.name = name
        self.birth_year = birth_year
        self.gender = gender
        self.age = 0
        self.phone = phone 
        self.time = datetime.now().strftime("%Y-%m-%d")
        self.medical_record = medical_record 

    def __str__(self):
        return f"患者 - | 患者 ID: {self.patient_id} | 名字: {self.name} | 性别: {self.gender} | 电话: {self.phone} | 时间: {self.time} |"
 
    def add_new_patient(self):
        self.age = calculate_patient_age(self.birth_year)
        clinic_storage.modify_system_log(f"新患者 - | {self.time:^20} | 患者 ID: {self.patient_id:^5} | 名字: {self.name:^15} | 电话: {self.phone} | 性别: {self.gender:^2} | 年龄: {self.age:^4} | 出生年: {self.birth_year} |")
        doctor_name = data_storage.doctor_storage.identify_doctor(self.doctor_id)
        data_storage.patient_storage.store_new_patient(self.patient_id, [doctor_name, self.name, self.gender, self.age, self.birth_year, self.phone, self.time, self.medical_record])
        data_storage.patient_symptom_storage.storage[self.patient_id] = [] # Create symptom data space
        clinic_storage_manager.clinic_storage.save_json(data_storage.patient_symptom_storage.storage, "patient_symptom_record.json")

    def delete_patient(self, patient_id):
        current_time = datetime.now().strftime("%Y-%m-%d")
        clinic_storage.modify_system_log(f"删除患者 - | {current_time:^20} | 患者 ID: {patient_id:^5} |")
        data_storage.patient_storage.delete_patient(patient_id, current_time) 

###############################################################################################################################

class Patient_Symptom:
    def __init__(self, patient_id, symptom_id, doctor_id, complaint,\
                  diagnosis, treatment_course, note):
        
        self.patient_id = patient_id
        self.symptom_id = symptom_id
        self.doctor_id = doctor_id
        self.complaint = complaint
        self.diagnosis = diagnosis
        self.treatment_course = treatment_course
        self.note = note
        self.diagnosis_time = datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"患者 - | 时间: {self.diagnosis_time} | 患者 ID: {self.patient_id} | 主诉: {self.complaint} | 临床诊断: {self.diagnosis} | 治疗过程: {self.treatment_course} | 备注: {self.note} |"

    def add_patient_symptom(self):
        clinic_storage.modify_system_log(f"新症状 - | {self.diagnosis_time:^20} | 患者 ID: {self.patient_id:^5} | 症状 ID: {self.symptom_id:^5} | 主诉: {self.complaint} | 临床诊断: {self.diagnosis} | 治疗过程: {self.treatment_course} | 备注: {self.note} |")
        data_storage.patient_symptom_storage.store_new_patient_symptom(self.patient_id, [self.symptom_id, self.doctor_id, self.complaint, self.diagnosis, self.treatment_course, self.note, self.diagnosis_time])

    def delete_symptom_log(self, symptom_id):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        clinic_storage.modify_system_log(f"删除症状 - | {current_time:^20} | 患者 ID: {self.patient_id:^5} | 症状 ID: {symptom_id:^5} | 临床诊断: {self.diagnosis:^20} | 备注: {self.note} |")
        data_storage.patient_symptom_storage.delete_patient_symptom(self.patient_id, str(symptom_id), current_time) 

###############################################################################################################################

class ToolKit:
    def __init__(self):
        self.count = 0

    def unique_count(self, storage_data: dict, date_ind: int) -> int:
        # Take out the last 60 patients in the storage_data
        # Match today's date with them one by one
        # return total number
        self.clear_count()
        search_ids = list(storage_data.keys())[-60:] 
        current_time = list(datetime.now().strftime("%Y-%m-%d").split('-')) # today's date

        for patient_id in search_ids:
            time = storage_data[patient_id][date_ind] 
            year, month, day = time[0:4], time[5:7], time[8:10] 
            if current_time[0] == year and current_time[1] == month and current_time[2] == day:
                # Patient ID was registered today
                self.count += 1 
        
        return self.count

    def clear_count(self):
        self.count = 0 

###############################################################################################################################

# data_storage.patient_symptom_storage.symptom_relationship() # Update symptom data
toolkit = ToolKit()