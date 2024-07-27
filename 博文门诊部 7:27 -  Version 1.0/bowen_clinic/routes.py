from flask import render_template, url_for, redirect, flash
from datetime import datetime
from bowen_clinic import app 
from . import models
from bowen_clinic.forms import PatientForm, SymptomForm

# Generate ID
import uuid 
def generate_unique_id():
    return str(uuid.uuid4())

# Import files
from . import data_storage
from datetime import datetime

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

@app.route("/patient/<string:patient_id>")
def patient(patient_id):
    patient = data_storage.patient_storage.storage[patient_id]
    symptoms = data_storage.patient_symptom_storage.storage[patient_id][::-1]
    return render_template('patient_info.html', patient=patient, symptoms=symptoms, patient_id=patient_id)  

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
    data_storage.patient_storage.delete_patient(patient_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    flash('此患者信息已被删除')
    return redirect(url_for('home_page')) 

@app.route("/patient/<string:patient_id>/add-symptom", methods=['GET', 'POST'])  
def add_patient_symptom(patient_id): 
    form = SymptomForm() 
    if form.validate_on_submit(): 
        symptom_id = generate_unique_id() # Unique id

        # patient_id, symptom_id, doctor_id, complaint, diagnosis, treatment_course, note
        patient_symptom_module = models.Patient_Symptom(patient_id, symptom_id, "0", form.complaint.data,\
                                                         form.diagnosis.data, form.treatment_course.data, form.note.data)
        patient_symptom_module.add_patient_symptom()

        flash('此诊断已被加入进数据库当中', 'success') 
        return redirect(url_for('patient', patient_id=patient_id)) 
    return render_template('add_patient_symptom.html', title='Add Patient Symptom', form=form) 

@app.route("/patient/<string:patient_id>/<string:symptom_id>/delete-symptom", methods=['GET', 'POST']) 
def delete_patient_detail(patient_id, symptom_id): 
    data_storage.patient_symptom_storage.delete_patient_symptom(patient_id, symptom_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    flash('此患者病患信息已被删除')
    return redirect(url_for('patient', patient_id=patient_id)) 