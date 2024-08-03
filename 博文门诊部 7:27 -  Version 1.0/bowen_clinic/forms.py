from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, TextAreaField
from wtforms.validators import DataRequired

# Input Data
class PatientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()]) 
    gender = SelectField('gender', choices=[('男', '男'), ('女', '女')]) 
    birth_year = IntegerField('birth_year') 
    phone = IntegerField('phone') 
    medical_record = StringField('medical_record')
    submit = SubmitField('添加')  

class SymptomForm(FlaskForm):
    complaint = StringField('complaint') 
    diagnosis = StringField('diagnosis')
    treatment_course = StringField('treatment_course')
    note = StringField('note')
    submit = SubmitField('添加') 

# Update Data
class UpdatePatientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])  
    phone = IntegerField('phone') 
    medical_record = StringField('medical_record')
    submit = SubmitField('更改')  

class UpdateSymptomForm(FlaskForm):
    complaint = StringField('complaint') 
    diagnosis = StringField('diagnosis')
    treatment_course = StringField('treatment_course')
    note = StringField('note')
    submit = SubmitField('更改') 