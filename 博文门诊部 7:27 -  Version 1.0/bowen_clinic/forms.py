from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired

class PatientForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()]) 
    gender = SelectField('gender', choices=[('男', '男'), ('女', '女')]) 
    birth_year = IntegerField('birth_year') 
    phone = IntegerField('phone') 
    medical_record = StringField('medical_record')
    submit = SubmitField('添加')  

class SymptomForm(FlaskForm):
    complaint = StringField('complaint', validators=[DataRequired()]) 
    diagnosis = StringField('diagnosis')
    treatment_course = StringField('treatment_course')
    note = StringField('note')
    submit = SubmitField('添加') 
