from flask import render_template, url_for, redirect, flash
from datetime import datetime
from bowen_clinic import app 
from . import clinic_storage_manager
from . import models
from . import data_storage
from bowen_clinic.forms import PatientForm, SymptomForm, UpdatePatientForm, UpdateSymptomForm
import uuid 


def calculate_patient_age(birth_year: str) -> str:
    return str(int(datetime.now().strftime("%Y")) - int(birth_year)) 

# Generate ID
def generate_unique_id():
    return str(uuid.uuid4())

@app.errorhandler(404)
def not_found(e):
  return render_template('404.html'), 404

@app.route("/")
def home_page():
    daily_unique_patient = models.toolkit.unique_count(data_storage.patient_storage.storage, -2)
    total_patient = len(data_storage.patient_storage.storage.keys())
    total_visit_count = models.toolkit.unique_count(data_storage.patient_symptom_storage.symptom_storage, -1)
    return render_template('find_patient.html', items=data_storage.patient_storage.storage, \
                                unique_patient = daily_unique_patient, total_visit_count = total_visit_count,\
                                total_patient = total_patient)

########################################################################################################################

# Patient

@app.route("/patient/<string:patient_id>")
def patient(patient_id):
    # [doctor_name, self.name, self.gender, self.birth_year, self.phone, self.time, self.medical_record]
    patients = data_storage.patient_storage.storage[patient_id]
    symptoms = data_storage.patient_symptom_storage.storage[patient_id][::-1]
    return render_template('patient_info.html', patient=patients, symptoms=symptoms, patient_id=patient_id)  

@app.route("/addpatient", methods=['GET', 'POST'])  
def add_patient(): 
    form = PatientForm() 
    if form.validate_on_submit(): 
        patient_id = generate_unique_id() # Unique id

        # patient_id, doctor_id, name, birth_year, gender, phone, home_address
        patient_module = models.Patient(patient_id, "0", form.name.data, form.birth_year.data, form.gender.data, form.phone.data, form.medical_record.data)
        patient_module.add_new_patient()

        flash('此患者已被加入进数据库当中', 'success') 
        return redirect(url_for('home_page')) 
    return render_template('add_patient.html', title='Add Patient', form=form) 

@app.route("/patient/<string:patient_id>/delete-patient", methods=['GET', 'POST']) 
def delete_patient(patient_id): 
    data_storage.patient_storage.delete_patient(patient_id, datetime.now().strftime("%Y-%m-%d"))
    flash('此患者信息已被删除')
    return redirect(url_for('home_page')) 

@app.route("/patient/<string:patient_id>/update-patient", methods=["Get", "Post"]) 
def update_patient(patient_id):
    patient = data_storage.patient_storage.storage[patient_id]
    # patient = ['崔美娟医生', '藏剑', '男', '1982', '00000000000', '2024-03-07', '']
    name, phone, medical_record = patient[1], patient[4], patient[6]
    form = UpdatePatientForm()

    # [doctor_name, self.name, self.gender, self.birth_year, self.phone, self.time, self.medical_record]
    if form.validate_on_submit():
        patient[1] = form.name.data
        patient[4] = form.phone.data
        patient[6] = form.medical_record.data 
        
        clinic_storage_manager.clinic_storage.save_json(data_storage.patient_storage.storage, "patient_data.json")
        clinic_storage_manager.clinic_storage.save_csv(data_storage.patient_storage.storage, "patient_data.csv")
        
        flash('此更改已被加入进数据库当中', 'success') 
        return redirect(url_for('patient', patient_id=patient_id)) 
    
    return render_template("update_patient.html",  title='Update Patient', form=form,\
                            name=name, phone=phone, medical_record=medical_record)

########################################################################################################################

# Patient Symptoms

@app.route("/patient/<string:patient_id>/add-symptom", methods=['GET', 'POST'])  
def add_patient_symptom(patient_id): 
    form = SymptomForm() 
    if form.validate_on_submit(): 
        symptom_id = generate_unique_id() # Unique id

        # patient_id, symptom_id, doctor_id, complaint, diagnosis, treatment_course, note
        patient_symptom_module = models.Patient_Symptom(patient_id, symptom_id, "0", form.complaint.data,\
                                                         form.diagnosis.data, form.treatment_course.data, form.note.data, form.time.data) 
        patient_symptom_module.add_patient_symptom()

        flash('此诊断已被加入进数据库当中', 'success') 
        return redirect(url_for('patient', patient_id=patient_id)) 
    return render_template('add_patient_symptom.html', title='Add Patient Symptom', form=form) 

@app.route("/patient/<string:patient_id>/<string:symptom_id>/delete-symptom", methods=['GET', 'POST']) 
def delete_patient_detail(patient_id, symptom_id): 
    data_storage.patient_symptom_storage.delete_patient_symptom(patient_id, symptom_id, datetime.now().strftime("%Y-%m-%d"))
    flash('此患者病患信息已被删除')
    return redirect(url_for('patient', patient_id=patient_id)) 

@app.route("/patient/<string:patient_id>/<string:symptom_id>/update-symptom", methods=["Get", "Post"]) 
def update_patient_symptom(patient_id, symptom_id):
    symptom = data_storage.patient_symptom_storage.symptom_storage[symptom_id]
    print("symptom:",symptom[1:5])
    complaint, diagnosis, treatment_course, note = symptom[1:5]
    form = UpdateSymptomForm()

    if form.validate_on_submit():

        # Update the data under patient_id in .storage
        data = [symptom for symptom in data_storage.patient_symptom_storage.storage[patient_id] if symptom[0] == symptom_id][0]
        storage_ind = data_storage.patient_symptom_storage.storage[patient_id].index(data) # Find index of symptom under patient
        data_storage.patient_symptom_storage.storage[patient_id][storage_ind][2] = form.complaint.data
        data_storage.patient_symptom_storage.storage[patient_id][storage_ind][3] = form.diagnosis.data
        data_storage.patient_symptom_storage.storage[patient_id][storage_ind][4] = form.treatment_course.data
        data_storage.patient_symptom_storage.storage[patient_id][storage_ind][5] = form.note.data
        data_storage.patient_symptom_storage.storage[patient_id][storage_ind][6] = form.time.data


        # Update the data under .symptom_storage
        data_storage.patient_symptom_storage.symptom_storage[symptom_id][1] = form.complaint.data
        data_storage.patient_symptom_storage.symptom_storage[symptom_id][2] = form.diagnosis.data
        data_storage.patient_symptom_storage.symptom_storage[symptom_id][3] = form.treatment_course.data
        data_storage.patient_symptom_storage.symptom_storage[symptom_id][4] = form.note.data
        data_storage.patient_symptom_storage.symptom_storage[symptom_id][5] = form.time.data

        # Back up
        clinic_storage_manager.clinic_storage.save_json(data_storage.patient_symptom_storage.storage, "patient_symptom_record.json")
        clinic_storage_manager.clinic_storage.save_csv(data_storage.patient_symptom_storage.symptom_storage, "patient_symptom_record.csv")
        
        flash('此更改已被加入进数据库当中', 'success') 
        return redirect(url_for('patient', patient_id=patient_id)) 
    
    return render_template("update_patient_symptom.html",  title='Update Patient', form=form,\
                           complaint=complaint, diagnosis=diagnosis, treatment_course=treatment_course, note=note)