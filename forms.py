from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, FileField,HiddenField, DateField, TimeField  
from wtforms.validators import DataRequired, Email, Length, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Fullname', validators=[DataRequired(), Length(max=100)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
    pincode = StringField('Pin Code', validators=[DataRequired(), Length(max=10)])
    # Make these fields optional since they're only for service professionals
    service_type = StringField('Service Type', validators=[Optional(), Length(max=100)])
    experience = IntegerField('Experience', validators=[Optional()])
    documents = FileField('Documents', validators=[Optional()])

class CustomerProfileForm(FlaskForm):
    address = StringField('Address', validators=[Length(max=200)])
    phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Update Profile')

class ServiceProfessionalProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100)])
    description = TextAreaField('Description')
    service_type = StringField('Service Type', validators=[Length(max=100)])
    experience = IntegerField('Experience')
    submit = SubmitField('Update Profile')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    price = StringField('Price', validators=[DataRequired()])
    time_required = IntegerField('Time Required (minutes)', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Add Service')

class ServiceRequestForm(FlaskForm):
    service_id = HiddenField('Service ID')
    preferred_date = DateField('Preferred Date', validators=[DataRequired()])
    preferred_time = TimeField('Preferred Time', validators=[DataRequired()])
    description = TextAreaField('Description/Special Instructions')
    address = TextAreaField('Service Address', validators=[DataRequired()])
    pincode = StringField('Pin Code', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit Request')