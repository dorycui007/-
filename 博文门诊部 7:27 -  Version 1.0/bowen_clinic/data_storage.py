# Store patient data, symptom data, etc 
# The models.py store all attributes of data but here all data are stored in temporary storage
# Use clinic_storage_manager.py to store to json/csv files

from . import clinic_storage_manager

###############################################################################################################################

class Doctor:
    def __init__(self):
        self.filename = "doctor_info.json"
        self.storage = clinic_storage_manager.clinic_storage.load_json(self.filename) 

    def identify_doctor(self, doctor_id: str) -> str:
        return self.storage[doctor_id][0] + "医生" # return doctor's name
    
    def store_new_doctor(self, doctor_id: int, doctor_info: list):
        # medicine info: [self.name, self.id_card, self.gender, self.age, self.home_address, self.time]
        self.storage[str(doctor_id)] = doctor_info
        clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)

    def delete_doctor(self, doctor_id: str, current_time: str):
        name = self.storage[doctor_id][0]
        del self.storage[doctor_id]
        clinic_storage_manager.clinic_storage.modify_system_log(f"删除医生 - | 时间: {current_time} | 医生 ID: {doctor_id} | 名字: {name} |") 
        clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)

###############################################################################################################################

class Patient:
    def __init__(self):
        self.filename = "patient_data.json"
        self.storage = clinic_storage_manager.clinic_storage.load_json(self.filename) # load patient_data.json 

    def store_new_patient(self, patient_id: int, patient_info: list):
        # patient info: [doctor_id, fullname, id_card, gender, age, home_address, record time, medical_record]
        # Patient_id are unique increasing integers: 0, 1, 2, ...
        self.storage[patient_id] = patient_info

        patient_symptom_storage.storage[patient_id] = []
        clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)
        clinic_storage.save_csv(self.storage, "patient_data.csv") 

    def delete_patient(self, patient_id, current_time):
        name = self.storage[patient_id][1]
        del self.storage[patient_id]
        clinic_storage_manager.clinic_storage.modify_system_log(f"删除患者 - | 时间: {current_time} | 患者 ID: {patient_id} | 名字: {name} |") 
        clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)

        # Once the patient is removed from the system
        # The symptom data should be removed also 

        # Removing symptom data 
        if patient_id in patient_symptom_storage.storage.keys():
            del patient_symptom_storage.storage[patient_id]
            clinic_storage_manager.clinic_storage.save_json(patient_symptom_storage.storage, patient_symptom_storage.filename)
            clinic_storage.save_csv(self.storage, "patient_data.csv") 
            clinic_storage_manager.clinic_storage.modify_system_log(f"All symptom data associate with Patient {patient_id} are removed.")

###############################################################################################################################

class Patient_Symptom:
    def __init__(self):
        self.filename = "patient_symptom_record.json"
        self.storage = clinic_storage_manager.clinic_storage.load_json(self.filename)  # patient_id: {[symptom_info1], [symptom_info2], ...}
        self.symptom_storage = {} # symptom_id: [self.doctor_id, self.full_name, self.result, self.sick_tag, self.medicine, self.medicine_description, self.medicine_price, self.diagnosis_time]

    def symptom_relationship(self):
        # This function must run first
        # Given the symptom_id being stored inside the array under the patient
        # This function can be used to extract the symptom_id under every patient

        for patient_id in self.storage.keys():
            patient_symptom = self.storage[patient_id]
            # patient_symptom: list -> 2-D array containing past symptoms of patient
            for symptom_info_id in range(len(patient_symptom)):
                id, info = patient_symptom[symptom_info_id][0], patient_symptom[symptom_info_id][1:]
                self.symptom_storage[id] = info 

    def store_new_patient_symptom(self, patient_id: str, symptom_info: list):
        # self.patient_id, [self.symptom_id, doctor_name, self.complaint, self.diagnosis, self.treatment_course, self.note, self.diagnosis_time]
        if patient_id in patient_storage.storage.keys():
            # patient exists
  
            self.storage[patient_id].append(symptom_info)   

            # symptom_info = [patient_id, self.doctor_id, self.full_name, self.result, self.sick_tag, self.medicine, self.medicine_description, self.medicine_price, self.diagnosis_time]
            # symptom_id = [patient_id, self.doctor_id, self.full_name, self.result, self.sick_tag, self.medicine, self.medicine_description, self.medicine_price, self.diagnosis_time]
            self.symptom_storage[symptom_info[0]] = symptom_info[1:] 
            clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)
            clinic_storage.save_csv(self.symptom_storage, "patient_symptom_record.csv") 

        else:
            raise Exception(f"(store_new_patient_symptom) Patient ID: {patient_id} does not exist.") 

    def delete_patient_symptom(self, patient_id: str, symptom_id: str, current_time: str):
        print(f"Deleting patient symptom ID: {symptom_id}")
        if patient_id in patient_storage.storage.keys(): # patient id exists 
            if symptom_id in self.symptom_storage.keys(): # symptom id exists 
                doctor_id = self.symptom_storage[symptom_id][0] 
                doctor = doctor_storage.identify_doctor(doctor_id)

                # Delete from symptom_storage
                del self.symptom_storage[symptom_id]

                # Delete from storage
                self.storage[patient_id] = [symptom_info for symptom_info in self.storage[patient_id] if symptom_info[0] != symptom_id]
                name = patient_storage.storage[patient_id][1]

                clinic_storage_manager.clinic_storage.modify_system_log(f"删除症状 - | 时间: {current_time} | 患者 ID: {patient_id} | 名字: {name} | 医生: {doctor} |") 
                clinic_storage_manager.clinic_storage.save_json(self.storage, self.filename)
                clinic_storage.save_csv(self.symptom_storage, "patient_symptom_record.csv") 
                
            else:
                raise Exception(f"(delete_patient_symptom) Symptom ID: {symptom_id} does not exist.")
        else:
            raise Exception(f"(delete_patient_symptom) Patient ID: {patient_id} does not exist.") 

###############################################################################################################################

doctor_storage = Doctor() 
patient_storage = Patient() 
patient_symptom_storage = Patient_Symptom() 

# Back up data to csv files
clinic_storage = clinic_storage_manager.ClinicStorage() 
patient_symptom_storage.symptom_relationship()