from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, IntegerField, FileField,HiddenField, DateField, TimeField, DecimalField
from wtforms.validators import DataRequired, Email, Length, Optional,NumberRange

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Fullname', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)]) 
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
    pincode = StringField('Pin Code', validators=[DataRequired(), Length(max=10)])
    service_type = StringField('Service Type', validators=[Optional(), Length(max=100)])
    experience = IntegerField('Experience', validators=[Optional()])
    documents = FileField('Documents', validators=[Optional()])

class CustomerProfileForm(FlaskForm):
    address = StringField('Address', validators=[Length(max=200)])
    phone = StringField('Phone', validators=[Length(max=20)])
    submit = SubmitField('Update Profile')

class ServiceProfessionalProfileForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=100)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    description = TextAreaField('Description')
    service_type = StringField('Service Type', validators=[Length(max=100)])
    experience = IntegerField('Experience')
    submit = SubmitField('Update Profile')

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Add Service')

class SubServiceForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    time_required = IntegerField('Time Required (minutes)', validators=[DataRequired(), NumberRange(min=0)])

class ServiceRequestForm(FlaskForm):
    service_id = HiddenField('Service ID')
    preferred_date = DateField('Preferred Date', validators=[DataRequired()])
    preferred_time = TimeField('Preferred Time', validators=[DataRequired()])
    description = TextAreaField('Description/Special Instructions')
    address = TextAreaField('Service Address', validators=[DataRequired()])
    pincode = StringField('Pin Code', validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Submit Request')

#class for rating_services

class ServiceRatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[
        DataRequired(),
        NumberRange(min=1, max=5, message="Rating must be between 1 and 5")
    ])
    feedback = TextAreaField('Feedback', validators=[
        Optional(),
        Length(max=500, message="Feedback must be less than 500 characters")
    ])